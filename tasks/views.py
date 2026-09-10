from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.utils import timezone

from .models import Task
from .forms import TaskForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = Task.objects.filter(user=self.request.user)
        today = timezone.now().date()

        ctx["total"] = qs.count()
        ctx["completed"] = qs.filter(completed=True).count()
        ctx["pending"] = qs.filter(completed=False).count()
        ctx["overdue"] = qs.filter(completed=False, due_date__lt=today).count()
        ctx["recent_tasks"] = qs.order_by("-created_at")[:5]
        ctx["upcoming"] = (
            qs.filter(completed=False, due_date__gte=today)
            .order_by("due_date")[:5]
        )
        return ctx


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)

        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        priority = self.request.GET.get("priority", "")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if status == "completed":
            qs = qs.filter(completed=True)
        elif status == "pending":
            qs = qs.filter(completed=False)
        if priority in ("low", "medium", "high"):
            qs = qs.filter(priority=priority)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["status"] = self.request.GET.get("status", "")
        ctx["priority"] = self.request.GET.get("priority", "")
        return ctx


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "New Task"
        ctx["button_text"] = "Create Task"
        return ctx


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Task updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Edit Task"
        ctx["button_text"] = "Save Changes"
        return ctx


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Task deleted.")
        return super().form_valid(form)


class TaskToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save(update_fields=["completed", "updated_at"])
        if task.completed:
            messages.success(request, f"Completed: {task.title}")
        else:
            messages.info(request, f"Reopened: {task.title}")
        return redirect(request.META.get("HTTP_REFERER", "tasks:list"))