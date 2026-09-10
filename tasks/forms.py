from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-input"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
        help_text="Pick a date and time",
    )

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
            "completed": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure the widget formats the existing value correctly
        if self.instance and self.instance.pk and self.instance.due_date:
            self.initial["due_date"] = self.instance.due_date.strftime("%Y-%m-%dT%H:%M")