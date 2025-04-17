from django import forms
from . import models

class TimeUserWindowForm(forms.ModelForm):
    time_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Время начала")
    time_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Время окончания")

    class Meta:
        model = models.TimeUserWindow
        fields = '__all__'