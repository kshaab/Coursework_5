from django.contrib import admin
from habits.models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "periodicity")
    list_filter = ("is_public",)
