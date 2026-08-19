from django import forms 
from .models import Task, Schedule

class TaskForm(forms.ModelForm):
    schedule = forms.ModelChoiceField(
        queryset=Schedule.objects.all(),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )

    class Meta:
        model = Task
        fields = ['schedule','title', 'description', 'duration_minutes', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows':3}),
            'duration_minutes': forms.NumberInput(attrs={'min': 0, 'class': 'input input-bordered w-full'}),
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox checkbox-primary'})
        }