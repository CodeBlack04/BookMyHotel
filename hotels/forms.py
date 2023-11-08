from django import forms

from django.core.exceptions import ValidationError
from datetime import date

INPUT_CLASSES = 'w-full mb-2 py-2 px-3 rounded-xl bg-gray-400 text-gray-800 border'

class BookRoomForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'placeholder': 'Enter your check-in date...',
        'class': INPUT_CLASSES
    }))

    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'placeholder': 'Enter your check-out date...',
        'class': INPUT_CLASSES
    }))

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('start_date')
        check_out = cleaned_data.get('end_date')

        if check_in and check_out:
            if check_in < date.today():
                raise ValidationError('The check-in date cannot be in the past.')
            
            if check_out < check_in:
                raise ValidationError("Check-out date must be after check-in date.")
            
        return cleaned_data