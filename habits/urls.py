from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateView, HabitDestroyView, HabitListView, HabitRetrieveView, HabitUpdateView

app_name = HabitsConfig.name

urlpatterns = [
    path("create/", HabitCreateView.as_view(), name="habit-create"),
    path("list/", HabitListView.as_view(), name="habits-list"),
    path("habit/<int:pk>", HabitRetrieveView.as_view(), name="habit-retrieve"),
    path("update/<int:pk>", HabitUpdateView.as_view(), name="habit-update"),
    path("delete/<int:pk>", HabitDestroyView.as_view(), name="habit-delete"),
]
