from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("tasks/", views.TaskListView.as_view(), name="list"),
    path("tasks/new/", views.TaskCreateView.as_view(), name="create"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("tasks/<int:pk>/toggle/", views.TaskToggleView.as_view(), name="toggle"),
]