from django.contrib import admin

from .models import CustomUser, Subscription

admin.site.empty_value_display = "-empty-"


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")
    list_filter = ("email", "username")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "influencer")
    list_filter = ("follower", "influencer")
