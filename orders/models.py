from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        IN_PROGRESS = 'In Progress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    order_number = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_man = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    delivery_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"
