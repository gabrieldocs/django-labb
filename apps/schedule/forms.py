from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'description','total_minutes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'total_minutes': forms.NumberInput(attrs={'class': 'input input bordered w-full'})
        }