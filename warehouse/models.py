from django.db import models
from django.utils import timezone
import datetime


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    temperature = models.FloatField()
    height = models.FloatField()
    features = models.TextField()
    description = models.TextField()
    contact = models.CharField(max_length=255)
    image = models.ImageField(upload_to="warehouse_images/")


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
    # user
    string_for_qr_code = models.UUIDField()

    @property
    def is_overdue(self):
        return self.end_date < timezone.now()

    @property
    def is_near_end(self):
        return self.end_date - timezone.now() < datetime.timedelta(days=2)
