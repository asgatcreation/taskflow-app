from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "What needs to be done?",
                "class": "form-input",
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Add more details (optional)",
                "rows": 4,
                "class": "form-input",
            }),
            "priority": forms.Select(attrs={"class": "form-input"}),
            "due_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-input",
            }),
            "completed": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }