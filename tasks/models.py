from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["completed", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tasks:list")

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False