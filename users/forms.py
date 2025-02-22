from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address', 'date_of_birth']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'phone_number', 'address', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# Budget Tracking and Summarization
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),  # Dropdown
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter source'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

from django import forms
from .models import BillPayment

class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = BillPayment
        fields = ['bill_name', 'amount', 'due_date', 'paid', 'reminder_type', 'reminder_category', 'reminder_date']
        widgets = {
            'bill_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the bill name',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the amount',
                'step': '0.01',  # For decimal input
                'min': '0',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'paid': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'reminder_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'reminder_category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'reminder_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'location', 'credit_card_number', 'risk_score']  # Updated field
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'risk_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }
