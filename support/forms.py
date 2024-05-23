from django import forms

from myauth.models import User


INPUT_CLASSES = 'w-full mb-4 py-4 px-6 rounded-xl text-gray-800 border'

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'password',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email address...',
                'class': INPUT_CLASSES
            }),

            'name': forms.TextInput(attrs={
                'placeholder': 'Name...',
                'class': INPUT_CLASSES
            }),

            'role': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Enter a password...',
                'class': INPUT_CLASSES
            }),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email address...',
                'class': INPUT_CLASSES
            }),

            'name': forms.TextInput(attrs={
                'placeholder': 'Name...',
                'class': INPUT_CLASSES
            }),

            'role': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
        }