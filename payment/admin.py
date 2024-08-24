from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(ShippingAddress)
# admin.site.register(Order)
admin.site.register(OrderItem)


# create order items inline
class OrderItemsInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['data_ordered']
    fields = ['user','full_name','shipping_address','amount_paid','data_ordered','shipped']
    inlines = [OrderItemsInline]


# unregister orderModel
# admin.site.unregister(Order)

# Re register Our Order AND OrderItems
admin.site.register(Order,OrderAdmin)
