from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "town")
    list_filter = ("town",)
    search_fields = ("email", "town")
