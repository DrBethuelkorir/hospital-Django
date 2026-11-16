# patients/forms.py
from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'address', 'phone_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
                'required': True,
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 35',
                'min': 0,
                'max': 150,
                'required': True,
            }),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter address',
                'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0700123456',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'patient@example.com',
                'required': True,
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Patient.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A patient with this email already exists.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0 or age > 150:
            raise forms.ValidationError("Enter a valid age between 0 and 150.")
        return age