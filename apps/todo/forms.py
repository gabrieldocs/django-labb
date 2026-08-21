from django import forms 
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # REMOVEU 'schedule' daqui para não exigir no formulário HTML
        fields = ['title', 'description', 'duration_minutes', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'duration_minutes': forms.NumberInput(attrs={'min': 0, 'class': 'input input-bordered w-full'}),
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox checkbox-primary'})
        }