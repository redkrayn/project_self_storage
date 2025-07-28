import datetime
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import Count, Exists, Max, Min, OuterRef
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from custom_user.models import CustomUser


class WarehouseManager(models.Manager):
    def with_cell_counts(self):
        return self.annotate(
            total_cells=Count("cells"),
            empty_cells=Count(
                "cells",
                filter=~Exists(
                    Order.objects.filter(
                        cell_id=OuterRef("cells__id"),
                        is_active=True,
                    )
                ),
                distinct=True,
            ),
            min_price=Min("cells__base_price_per_meter"),
            max_height=Max("cells__height"),
        )


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    temperature = models.FloatField()
    height = models.FloatField()
    features = models.TextField()
    description = models.TextField()
    contact = models.CharField(max_length=255)
    image = models.ImageField(upload_to="warehouse_images/")

    objects = WarehouseManager()

    def __str__(self):
        return f"{self.name} {self.address}"


class Cell(models.Model):
    cell_id = models.CharField(max_length=255, unique=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="cells"
    )
    base_price_per_meter = models.FloatField(default=2000)
    floor = models.IntegerField()
    width = models.FloatField()
    length = models.FloatField()
    height = models.FloatField()

    @property
    def price(self):
        return self.base_price_per_meter * self.width * self.length

    @property
    def area(self):
        return self.width * self.length


def month_more():
    return timezone.now() + timezone.timedelta(days=30)


class Order(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name="orders")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=month_more)
    price_per_day_overdue = models.FloatField(default=100)
    last_overdue_notification = models.DateTimeField(
        null=True, blank=True, verbose_name="Уведомление о просрочке"
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="orders"
    )
    string_for_qr_code = models.UUIDField(default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    adv_id = models.IntegerField(null=True, blank=True)

    @property
    def is_overdue(self):
        return self.end_date < timezone.now()

    @property
    def is_near_end(self):
        return self.end_date - timezone.now() < datetime.timedelta(days=2)


class Request(models.Model):
    email = models.EmailField()
    status = models.CharField(max_length=255, default="new")
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Order)
def send_order_creation_email(sender, instance, created, **kwargs):
    if created:
        user_email = instance.user.email
        warehouse_name = instance.cell.warehouse.name
        cell_id = instance.cell.cell_id
        start_date = instance.start_date.strftime("%d.%m.%Y")
        end_date = instance.end_date.strftime("%d.%m.%Y")

        subject = f"Ваш заказ успешно создан"
        message = f"""
        Здравствуйте!

        Ваш заказ на аренду ячейки успешно оформлен:

        Склад: {warehouse_name}
        Ячейка: {cell_id}
        Дата начала: {start_date}
        Дата окончания: {end_date}
        Стоимость: {instance.price_per_day_overdue} руб./день

        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
