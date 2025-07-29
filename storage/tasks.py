import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import models
from warehouse.models import Order


@shared_task
def check_overdue_orders():
    now = timezone.now()

    overdue_orders = Order.objects.filter(
        end_date__lt=now
    ).filter(
        models.Q(last_overdue_notification__isnull=True) |
        models.Q(last_overdue_notification__lte=now - timezone.timedelta(days=30))
    )

    for order in overdue_orders:
        user_email = order.user.email
        warehouse_name = order.cell.warehouse.name
        cell_id = order.cell.cell_id
        end_date = order.end_date.strftime("%d.%m.%Y")

        subject = "Просрочен срок аренды ячейки"
        message = f"""
        Здарова зёма!

        Срок аренды ячейки истек ма бой:

        Склад: {warehouse_name}
        Ячейка: {cell_id}
        Дата окончания: {end_date}

        Ваши вещи будут храниться 6 месяцев от даты просрочки по чуть повышенному тарифу, после
        чего в случае, если Вы их не заберёте – Ваши вещи будут утеряны.

        Пожалуйста, свяжитесь с нами для решения вопроса.
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        order.last_overdue_notification = now
        order.save()


@shared_task
def send_rent_reminders():
    now = timezone.now()

    intervals = [
        (14, 'reminder_14d_sent'),
        (7, 'reminder_7d_sent'),
        (3, 'reminder_3d_sent'),
    ]

    for days, field_name in intervals:
        target_date = now + datetime.timedelta(days=days)
        start_range = target_date - datetime.timedelta(days=1)
        end_range = target_date + datetime.timedelta(days=1)

        orders = Order.objects.filter(
            end_date__gte=start_range,
            end_date__lte=end_range,
        ).filter(
            **{f'{field_name}__isnull': True}
        )

        for order in orders:
            user_email = order.user.email
            warehouse_name = order.cell.warehouse.name
            cell_id = order.cell.cell_id
            end_date = order.end_date.strftime("%d.%m.%Y")

            subject = f"Напоминание: аренда истекает через {days} дней"
            message = f"""
            Здарова зёма!

            Напоминаем, что срок аренды ячейки заканчивается через {days} дней:

            Склад: {warehouse_name}
            Ячейка: {cell_id}
            Дата окончания: {end_date}
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )

            setattr(order, field_name, now)
            order.save()
