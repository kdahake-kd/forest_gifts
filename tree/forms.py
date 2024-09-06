from django import forms
from .models import Individual, CollegeStudent, IndustryOrganization

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['name', 'date_of_birth', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
        }

class CollegeStudentForm(forms.ModelForm):
    class Meta:
        model = CollegeStudent
        fields = ['name', 'date_of_birth', 'address', 'college']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'college': forms.Select(attrs={'class': 'form-control'}),
        }

class IndustryOrganizationForm(forms.ModelForm):
    class Meta:
        model = IndustryOrganization
        fields = ['name', 'date_of_birth', 'address', 'organization_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your organization\'s name'}),
        }

