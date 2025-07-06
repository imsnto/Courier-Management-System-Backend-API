from django.contrib import admin

from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'delivery_man', 'status', 'created_at', 'updated_at')
