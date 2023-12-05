from django.contrib import admin

from .models import Subscription


class EmptyValueDisplay(admin.ModelAdmin):
    empty_value_display = "-empty-"


@admin.register(Subscription)
class SubscriptionAdmin(EmptyValueDisplay):
    list_display = ("id", "follower", "influencer")
