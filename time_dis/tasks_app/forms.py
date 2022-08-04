from django import forms
from .models import Tasks


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'comment', 'category', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название задачи...'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите подробности к задаче..'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберете категорию задачи...'}),
            'priority': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберете приоритет для задачи..'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local',
                                               'placeholder': 'Установите срок выполнения...'})
        }
