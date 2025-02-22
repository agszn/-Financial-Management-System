from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', _('Enter a valid phone number.'))]
    )
    is_verified = models.BooleanField(_('email verified'), default=False)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        default='profile_pics/default.jpg', 
        blank=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Notification(models.Model):
    user_email = models.EmailField()
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user_email}"

from django.db import models
from decimal import Decimal
from datetime import date
from django.conf import settings

# Expense model
class Expense(models.Model):
    # Define categories as a tuple of tuples
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Bills', 'Bills'),
        ('Entertainment', 'Entertainment'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Utilities', 'Utilities'),
        ('Shopping', 'Shopping'),
        ('Miscellaneous', 'Miscellaneous'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='expenses',
        null=True
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,  # Dropdown of categories
        default='Other',
    )
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)  # Default to today's date, editable

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount} on {self.date}"

# Income model
class Income(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='incomes',
        null=True
    )
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)  # Default to today's date, editable

    def __str__(self):
        return f"{self.user.username} - {self.source} - ₹{self.amount} on {self.date}"

# BillPayment model
class BillPayment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bill_payments',
        null=True
    )
    REMINDER_CHOICES = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Specific', 'Specific'),
    ]

    REMINDER_CATEGORIES = [
        ('EMI', 'EMI Payment'),
        ('Credit Card', 'Credit Card Payment'),
        ('Insurance', 'Insurance Payment'),
        ('Tax', 'Tax Payment'),
        ('General', 'General Payment'),
    ]

    bill_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    reminder_type = models.CharField(max_length=10, choices=REMINDER_CHOICES, default='Specific')
    reminder_category = models.CharField(max_length=20, choices=REMINDER_CATEGORIES, default='General')
    reminder_date = models.DateField(null=True, blank=True)  # For specific reminders
    last_reminder_sent = models.DateField(null=True, blank=True)  # To track reminders sent
    
    
    def is_reminder_due(self):
        # Check if the reminder is due based on the reminder type
        if self.reminder_type == 'Specific' and self.reminder_date:
            return self.reminder_date == date.today()
        elif self.reminder_type == 'Weekly' and self.last_reminder_sent:
            return (date.today() - self.last_reminder_sent).days >= 7
        elif self.reminder_type == 'Monthly' and self.last_reminder_sent:
            return (
                (date.today().month != self.last_reminder_sent.month) or
                (date.today().year != self.last_reminder_sent.year)
            )
        return False

    def __str__(self):
        return f"{self.user.username} - {self.bill_name} ({self.reminder_category}) - ₹{self.amount} (Paid: {self.paid})"

# Budget model
from django.db.models import Sum

class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='budget',
        null=True
    )
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)  # Default to today's date, editable

    def calculate_remaining_budget(self):
        # Calculate total expenses for the current month
        total_expenses = Expense.objects.filter(
            date__month=self.updated_at.month,
            date__year=self.updated_at.year,
            user=self.user
        ).aggregate(total=Sum('amount'))['total'] or Decimal(0)

        # Calculate total paid bills for the current month
        total_paid_bills = BillPayment.objects.filter(
            due_date__month=self.updated_at.month,
            due_date__year=self.updated_at.year,
            user=self.user,
            paid=True
        ).aggregate(total=Sum('amount'))['total'] or Decimal(0)

        # Calculate the remaining budget
        return self.monthly_budget - (total_expenses + total_paid_bills)

    def is_budget_exceeded(self):
        # Check if the remaining budget is negative
        return self.calculate_remaining_budget() < 0

    def __str__(self):
        return f"{self.user.username}'s Budget"

# CreditCardFraudDetection
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    credit_card_number = models.CharField(max_length=16)  # Updated field
    flagged = models.BooleanField(default=False)
    risk_score = models.FloatField(default=0)

    def __str__(self):
        return f"Transaction {self.id} by {self.user.username}"

class FraudAlert(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"Fraud Alert for Transaction {self.transaction.id}"

class Blacklist(models.Model):
    credit_card_number = models.CharField(max_length=16, unique=True)
    reason = models.TextField()

    def __str__(self):
        return f"Blacklisted Credit Card: {self.credit_card_number}"


class AdminNotification(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"Notification for Transaction {self.transaction.id}"
