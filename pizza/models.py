from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from jwt_auth.models import Customer

sizes = ['Slice', 'Small', 'Medium', 'Large', 'Giant', 'Monster']
order_status = ['Pending', 'In the Kitchen', 'Prepared', 'Out for Delivery', 'Delivered']
SIZE_CHOICES = [(size, size) for size in sizes]
ORDER_STATUS_CHOICES = [(status, status) for status in order_status]


class Pizza(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, unique=True)
    size = models.CharField(choices=SIZE_CHOICES, default='Small', max_length=40)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    image = models.TextField(blank=False)
    ingridients = ArrayField(models.CharField(max_length=100))
    description = models.TextField(default="A Pizza to Have in Every Mood")

    def __str__(self) -> str:
        return self.name


    class Meta:
        db_table = 'Pizza'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_amount = models.IntegerField(default=0)
    ordered_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=False, default="Dine In")
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=40, default="Pending")
    pizzas = ArrayField(models.JSONField(), null=False, blank=False)
    ordered_by = models.ForeignKey(
        "jwt_auth.Customer", related_name='customer', on_delete=models.CASCADE, blank=False)

    class Meta:
        db_table = "Order"
