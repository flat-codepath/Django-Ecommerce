from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
admin.site.register(Category)
from django.contrib.auth.models import User

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline]


# unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)

# @admin.register()
# class profileAdmin(admin.ModelAdmin):
#     list_display = []
