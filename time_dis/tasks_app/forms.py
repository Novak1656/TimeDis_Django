from django import forms
from .models import Tasks, Subtasks


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'comment', 'category', 'priority', 'deadline', 'remind_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название задачи...'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберете категорию задачи...'}),
            'priority': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберете приоритет для задачи..'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local',
                                               'placeholder': 'Установите срок выполнения...'}),
            'remind_type': forms.Select(attrs={'class': 'form-control'})
        }


class SubtasksForm(forms.ModelForm):
    class Meta:
        model = Subtasks
        fields = ['title', 'comment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название подзадачи...'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'})
        }
