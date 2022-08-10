from django import forms
from tasks_app.models import Tasks


class TransferForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': "datetime-local"})
        }
