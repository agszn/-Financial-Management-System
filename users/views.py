import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .utils import send_email
import random


from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import *

from django.shortcuts import render, redirect,  get_object_or_404

# views.py
from django.shortcuts import render
from django.db.models import Sum
from .models import Income, Expense, BillPayment
from datetime import date


CustomUser = get_user_model()


# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP function
def send_otp_email(email, otp):
    subject = "Your OTP for Registration"
    message = f"Your OTP is: {otp}. It will expire in 5 minutes."
    from django.conf import settings
    from django.core.mail import send_mail
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# Registration View with OTP Confirmation
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            request.session['user_data'] = {
                'username': user.username,
                'password': request.POST['password1'],
                'email': user.email,
            }
            otp = generate_otp()
            request.session['otp'] = otp
            send_otp_email(user.email, otp)
            messages.success(request, "OTP sent to your email. Confirm to complete registration.")
            return redirect('confirm_otp')
    else:
        form = CustomUserForm()
    return render(request, 'users/register.html', {'form': form})

# OTP Confirmation View
def confirm_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_data = request.session.get('user_data')
        if user_otp == session_otp:
            CustomUser.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email']
            )
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Try again.")
    return render(request, 'users/confirm_otp.html')


# Base View
def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'index/index2.html')

# Home View (Requires Login)
@login_required
def home(request):
    return render(request, 'users/home.html')

# Custom Login View with OTP
def login_with_otp(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.get_user().email
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            send_otp_email(email, otp)
            messages.success(request, "OTP sent to your email. Confirm to log in.")
            return redirect('confirm_login_otp')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Confirm OTP for Login
def confirm_login_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        email = request.session.get('email')
        if user_otp == session_otp:
            user = CustomUser.objects.get(email=email)
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        messages.error(request, "Invalid OTP. Try again.")
    return render(request, 'users/confirm_otp.html')


# Password Change View
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})

# Welcome Email Example (Optional)
def welcome_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subject = "Welcome to Our Platform"
            message = "Thank you for registering. We're glad to have you!"
            if send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email]):
                messages.success(request, "Welcome email sent successfully!")
            else:
                messages.error(request, "Failed to send the welcome email.")
        return render(request, 'users/welcome_email.html')

# Logout View
def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')



# Edit user profile view
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def profile_view(request):
    user = request.user
    # Try to fetch the user's profile
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
        created = True
    else:
        created = False

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = CustomUserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'profile/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# Delete account view
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Delete the associated profile as well
        user.profile.delete()  # If the user has a profile
        user.delete()  # Delete the user
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  # Redirect to the home page after deletion
    return render(request, 'profile/delete_account.html')


# Password reset views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'profile/password_reset.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'profile/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'profile/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'profile/password_reset_complete.html'



from django.http import JsonResponse
from django.db.models import Sum
from decimal import Decimal
from datetime import date
from .models import Income, Expense, BillPayment, Budget
from django.http import JsonResponse
from django.db.models import Sum
from decimal import Decimal
from datetime import date
from .models import Income, Expense, BillPayment, Budget

@login_required
def chatbot(request):
    message = request.GET.get("message", "").strip().lower()

    # Define keywords mapping to actions or responses
    keyword_mapping = {
        "income": "what is my income",
        "expense": "what is my expense",
        "budget": "what is my budget",
        "bills": "what are my bills",
        "due bills": "which bills are due",
        "income sources": "which income sources do i have",
        "invest": "where to invest",
        "sip": "what is sip",
        "bonds": "what are bonds",
        "stocks": "what are stocks",
        "savings": "tips on savings",
        "returns": "what are returns",
    }

    # Match keywords in the user's message
    matched_key = None
    for keyword, mapped_question in keyword_mapping.items():
        if keyword in message:
            matched_key = mapped_question
            break

    try:
        if matched_key == "what is my income":
            total_income = Income.objects.filter(
                date__month=date.today().month,
                date__year=date.today().year,
            ).aggregate(total=Sum('amount'))['total'] or Decimal(0)
            response = f"Your total income this month is ₹{total_income}."

        elif matched_key == "what is my expense":
            total_expenses = Expense.objects.filter(
                date__month=date.today().month,
                date__year=date.today().year,
            ).aggregate(total=Sum('amount'))['total'] or Decimal(0)
            response = f"Your total expenses this month are ₹{total_expenses}."

        elif matched_key == "what is my budget":
            user_budget = Budget.objects.first()
            if user_budget:
                response = f"Your budget for this month is ₹{user_budget.monthly_budget}."
            else:
                response = "You don't have a budget set up yet."

        elif matched_key == "what are my bills":
            bills = BillPayment.objects.all()
            if bills.exists():
                bills_info = "\n".join([f"{bill.bill_name} - ₹{bill.amount}" for bill in bills])
                response = f"Your bills are:\n{bills_info}"
            else:
                response = "You don't have any bills at the moment."

        elif matched_key == "which bills are due":
            due_bills = BillPayment.objects.filter(
                due_date__gte=date.today(),
                paid=False,
            )
            if due_bills.exists():
                bills_info = "\n".join([f"{bill.bill_name} due on {bill.due_date} - ₹{bill.amount}" for bill in due_bills])
                response = f"Your upcoming due bills are:\n{bills_info}"
            else:
                response = "You don't have any unpaid bills due."

        elif matched_key == "which income sources do i have":
            income_sources = Income.objects.values('source').distinct()
            if income_sources.exists():
                sources_info = "\n".join([f"Source: {income['source']}" for income in income_sources])
                response = f"Your income sources are:\n{sources_info}"
            else:
                response = "You don't have any income sources recorded."

        elif matched_key == "where to invest":
            response = "Some popular investment options include: Mutual Funds, Stock Market, Real Estate, Bonds, and Gold."

        elif matched_key == "what is sip":
            response = "SIP (Systematic Investment Plan) is a method of investing a fixed amount regularly in mutual funds."

        elif matched_key == "what are bonds":
            response = "Bonds are debt securities where you lend money to the government or corporations in exchange for periodic interest payments and the return of principal at maturity."

        elif matched_key == "what are stocks":
            response = "Stocks represent ownership in a company. When you buy stocks, you own a small part of the company."

        elif matched_key == "tips on savings":
            response = "Some tips on savings include: automating your savings, creating an emergency fund, cutting unnecessary expenses, and investing in high-interest savings accounts or fixed deposits."

        elif matched_key == "what are returns":
            response = "Returns are the profits or income generated from an investment over time, often expressed as a percentage."

        else:
            response = "Sorry, I didn't understand your question. Try asking about 'income', 'expense', 'budget', 'bills', or 'due dates'."

    except Exception as e:
        response = f"Sorry, something went wrong. Error: {str(e)}"

    return JsonResponse({"response": response})


def chat(request):
    return render(request, 'chat/conv.html')

# dashboard 
from django.shortcuts import render
from django.db.models import Sum
from datetime import date
from decimal import Decimal
from .models import Expense, Income, BillPayment, Budget
from django.db.models import Sum
from decimal import Decimal

from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, BillPayment, Budget

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal

from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from .models import Expense, Income, BillPayment, Budget


# def dashboard(request):
#     # Expense breakdown
#     expenses_by_category = Expense.objects.values('category').annotate(total=Sum('amount'))
#     expense_data = [(item['category'], item['total']) for item in expenses_by_category]

#     # Total Income and Expenses
#     total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or Decimal(0)
#     total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or Decimal(0)

#     # Bills Due and Paid
#     bills_due = BillPayment.objects.filter(paid=False).aggregate(total=Sum('amount'))['total'] or Decimal(0)
#     paid_bills = BillPayment.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or Decimal(0)

#     # Budget related calculations
#     user_budget = Budget.objects.filter(user=request.user).first()
#     monthly_budget = user_budget.monthly_budget if user_budget else Decimal(0)

#     # Remaining Budget Calculation
#     remaining_budget = monthly_budget - (total_expenses + paid_bills)

#     # In-Balance Budget Calculation
#     in_balance_budget = total_expenses + paid_bills

#     context = {
#         'expense_data': expense_data,
#         'total_income': total_income,
#         'total_expenses': total_expenses,
#         'bills_due': bills_due,
#         'paid_bills': paid_bills,
#         'monthly_budget': monthly_budget,
#         'remaining_budget': remaining_budget,
#         'in_balance_budget': in_balance_budget,
#     }

#     return render(request, 'dashboard/dashboard.html', context)
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from decimal import Decimal
@login_required
def dashboard(request):
    # Expense breakdown
    expenses_by_category = Expense.objects.values('category').annotate(total=Sum('amount'))
    expense_data = [(item['category'], item['total']) for item in expenses_by_category]

    # Total Income and Expenses
    total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or Decimal(0)
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or Decimal(0)

    # Bills Due and Paid
    bills_due = BillPayment.objects.filter(paid=False).aggregate(total=Sum('amount'))['total'] or Decimal(0)
    paid_bills = BillPayment.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or Decimal(0)

    # Budget related calculations
    user_budget = Budget.objects.filter(user=request.user).first()
    monthly_budget = user_budget.monthly_budget if user_budget else Decimal(0)

    # Remaining Budget Calculation
    remaining_budget = monthly_budget - (total_expenses + paid_bills)

    # In-Balance Budget Calculation
    in_balance_budget = total_expenses + paid_bills

    # Prepare data for the email
    email_data = {
        'expense_data': expense_data,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'bills_due': bills_due,
        'paid_bills': paid_bills,
        'monthly_budget': monthly_budget,
        'remaining_budget': remaining_budget,
        'in_balance_budget': in_balance_budget,
        'user': request.user,
    }

    # Send the report via email
    subject = 'Your Financial Dashboard Report'
    recipient_email = request.user.email
    send_report_email(subject, email_data, recipient_email)

    context = email_data

    return render(request, 'dashboard/dashboard.html', context)


def send_report_email(subject, email_data, recipient_email):
    """Send an email with the financial report included as HTML."""
    # Render the email body using the same template
    email_body = render_to_string('dashboard/report_template.html', email_data)
    
    # Create and send the email
    email = EmailMessage(
        subject=subject,
        body=email_body,
        to=[recipient_email],
    )
    email.content_subtype = "html"  # Set email content type to HTML
    email.send()

# Expense Views
@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'tracker/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/expense_form.html', {'form': form})

@login_required
def expense_update(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/expense_form.html', {'form': form})

@login_required
def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'tracker/expense_confirm_delete.html', {'expense': expense})


# Income Views
@login_required
def income_list(request):
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'finance/income_list.html', {'incomes': incomes})

@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'finance/income_form.html', {'form': form})

@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'finance/income_form.html', {'form': form})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'finance/income_confirm_delete.html', {'income': income})

# Bill Payment Views
@login_required
def bill_list(request):
    bills = BillPayment.objects.all().order_by('due_date')
    return render(request, 'finance/bill_list.html', {'bills': bills})

@login_required
def bill_create(request):
    if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillPaymentForm()
    return render(request, 'finance/bill_form.html', {'form': form})

@login_required
def bill_update(request, pk):
    bill = get_object_or_404(BillPayment, pk=pk)
    if request.method == 'POST':
        form = BillPaymentForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillPaymentForm(instance=bill)
    return render(request, 'finance/bill_form.html', {'form': form})

@login_required
def bill_delete(request, pk):
    bill = get_object_or_404(BillPayment, pk=pk)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'finance/bill_confirm_delete.html', {'bill': bill})


from django.shortcuts import render, redirect, get_object_or_404
from .models import BillPayment, Notification
from .forms import BillPaymentForm
from django.http import JsonResponse
from datetime import date


# View to add or edit a bill
@login_required
def bill_form(request, bill_id=None):
    bill = get_object_or_404(BillPayment, id=bill_id) if bill_id else None
    if request.method == 'POST':
        form = BillPaymentForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bill_list')
    else:
        form = BillPaymentForm(instance=bill)
    return render(request, 'finance/bill_form.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from .models import Budget, Expense

@login_required
def manage_budget(request):
    # Retrieve or create budget for the user
    budget, created = Budget.objects.get_or_create(
        user=request.user, 
        defaults={'monthly_budget': Decimal('0.00')}  # Provide a default value
    )

    if request.method == 'POST':
        new_budget = request.POST.get('monthly_budget')
        if new_budget:
            budget.monthly_budget = Decimal(new_budget)
            budget.save()
            return redirect('manage_budget')

    # Calculate current month's expenses
    total_expenses = Expense.objects.filter(
        date__month=budget.updated_at.month,
        date__year=budget.updated_at.year,
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Convert monthly_budget to Decimal
    monthly_budget = Decimal(budget.monthly_budget)
    remaining_budget = monthly_budget - total_expenses
    is_exceeded = remaining_budget < 0

    context = {
        'budget': budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'is_exceeded': is_exceeded,
    }
    return render(request, 'budget/manage_budget.html', context)

# fraudDetection
from django.shortcuts import render
from .models import Transaction

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transaction/transaction_history.html', {'transactions': transactions})

# 101224

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Transaction, FraudAlert, Blacklist
from django.core.mail import send_mail

def is_admin(user):
    return user.is_staff
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

# # Create a new transaction
# @login_required
# def transaction_create(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.user = request.user
#             transaction.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm()
#     return render(request, 'transaction/CreateUpdate.html', {'form': form})

# # List all transactions
# @login_required
# def transaction_list(request):
#     transactions = Transaction.objects.filter(user=request.user)
#     return render(request, 'transaction/list.html', {'transactions': transactions})

# # Update a transaction
# @login_required
# def transaction_update(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
#     if request.method == 'POST':
#         form = TransactionForm(request.POST, instance=transaction)
#         if form.is_valid():
#             form.save()
#             return redirect('transaction_list')
#     else:
#         form = TransactionForm(instance=transaction)
#     return render(request, 'transaction/CreateUpdate.html', {'form': form})

# # Delete a transaction
# @login_required
# def transaction_delete(request, pk):
#     transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
#     if request.method == 'POST':
#         transaction.delete()
#         return redirect('transaction_list')
#     return render(request, 'transaction/delete.html', {'transaction': transaction})


# @login_required
# def flag_transaction(request, transaction_id):
#     transaction = get_object_or_404(Transaction, id=transaction_id)
#     transaction.flagged = True
#     transaction.save()

#     # Create Fraud Alert
#     FraudAlert.objects.create(transaction=transaction, message="Suspicious transaction detected.")

#     # Notify User
#     send_mail(
#         'Fraud Alert',
#         f"Suspicious transaction detected: ID {transaction.id}, Amount: {transaction.amount}",
#         '@gmail.com',
#         [transaction.user.email],
#         fail_silently=False,
#     )

#     return JsonResponse({'status': 'Transaction flagged'})

# @user_passes_test(is_admin)
# def blacklist_ip(request, ip_address):
#     Blacklist.objects.create(ip_address=ip_address, reason="Fraudulent activity")
#     return JsonResponse({'status': 'IP blacklisted'})

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Transaction, FraudAlert, Blacklist
from .forms import TransactionForm


# Create a new transaction
from django.shortcuts import redirect

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            # Check risk score
            if transaction.risk_score > 7:
                transaction.flagged = True
                transaction.save()
                send_fraud_alert(transaction, "High-risk score detected.")
                AdminNotification.objects.create(
                    transaction=transaction,
                    message="High-risk score detected."
                )
                return redirect('alert')

            # Check for multiple transactions from the same credit card
            today = now().date()
            same_card_count = Transaction.objects.filter(
                credit_card_number=transaction.credit_card_number,
                date__date=today
            ).count()

            if same_card_count >= 3:
                Blacklist.objects.get_or_create(credit_card_number=transaction.credit_card_number, reason="Multiple suspicious transactions.")
                send_admin_notification(transaction, f"Credit card {transaction.credit_card_number} has been blacklisted for suspicious activity.")
                AdminNotification.objects.create(
                    transaction=transaction,
                    message=f"Credit card {transaction.credit_card_number} has been blacklisted for suspicious activity."
                )
                return redirect('alert')

            # Check for large transactions
            if transaction.amount > 50000:
                send_admin_notification(transaction, "User marked for caution: Large transaction detected.")
                AdminNotification.objects.create(
                    transaction=transaction,
                    message="User marked for caution: Large transaction detected."
                )
                return redirect('alert')

            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transaction/CreateUpdate.html', {'form': form})




# List all transactions
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transaction/list.html', {'transactions': transactions})


# Update a transaction
@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)

            # Repeat fraud checks if updated
            if transaction.risk_score > 7:
                transaction.flagged = True
                send_fraud_alert(transaction, "High-risk score detected.")

            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transaction/CreateUpdate.html', {'form': form})


# Delete a transaction
@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transaction/delete.html', {'transaction': transaction})


# previous transactions
@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transaction/previous_transaction.html', {'transactions': transactions})


from django.http import Http404
from django.contrib import messages

@login_required
def transaction_detail(request, transaction_id):
    try:
        # Attempt to retrieve the transaction
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    except Http404:
        # Handle case where the transaction does not exist or does not belong to the user
        messages.error(request, "Transaction not found or you do not have permission to view it.")
        return redirect('transaction_list')
    except Exception as e:
        # Handle any other unexpected exceptions
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('transaction_list')

    return render(request, 'transaction/transaction_detail.html', {'transaction': transaction})


# Flag a transaction manually
@login_required
def flag_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.flagged = True
    transaction.save()
    send_fraud_alert(transaction, "Transaction flagged manually.")
    return JsonResponse({'status': 'Transaction flagged'})


@user_passes_test(lambda u: u.is_superuser)
def blacklist_credit_card(request, credit_card_number):
    # Ensure the credit card number is blacklisted
    Blacklist.objects.get_or_create(
        credit_card_number=credit_card_number,
        reason="Fraudulent activity"
    )
    return JsonResponse({'status': 'Credit card blacklisted', 'credit_card_number': credit_card_number})

    

# Helper functions
def send_fraud_alert(transaction, message):
    FraudAlert.objects.create(transaction=transaction, message=message)
    send_mail(
        'Fraud Alert',
        f"Fraud detected for Transaction {transaction.id}: {message}",
        '@gmail.com',
        [transaction.user.email],
        fail_silently=False,
    )


def send_admin_notification(transaction, message):
    # Simulating admin notification (could be expanded to include notification system)
    print(f"Admin notified: {message}")



@login_required
def alert(request):
    return render(request, 'notification/alert.html')

@login_required
def admin_notifications(request):
    notifications = AdminNotification.objects.all().order_by('-created_at')
    return render(request, 'notification/notification.html', {'notifications': notifications})


@login_required
def fraud_alerts(request):
    alerts = FraudAlert.objects.all().order_by('-created_at')
    return render(request, 'notification/fraud_alerts.html', {'alerts': alerts})

@login_required
def blacklisted_credit_card_number(request):
    blacklist = Blacklist.objects.all().order_by('credit_card_number')
    return render(request, 'notification/blacklisted_credit_card_number.html', {'blacklist': blacklist})


from django.db.models import Count

from django.shortcuts import render
from .models import Transaction, FraudAlert
from django.db.models import Count

import os
import seaborn as sns
import matplotlib.pyplot as plt
from django.conf import settings
from django.db.models import Count
from django.http import JsonResponse
from .models import Transaction, FraudAlert

def generate_graphs():
    # Create the directory for saving graphs
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'graphs')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Data for transactions by date
    transaction_counts = Transaction.objects.values('date__date').annotate(count=Count('id')).order_by('date__date')
    dates = [entry['date__date'] for entry in transaction_counts]
    counts = [entry['count'] for entry in transaction_counts]

    # Create transaction graph
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=dates, y=counts, marker='o')
    plt.title('Transactions by Date')
    plt.xlabel('Date')
    plt.ylabel('Number of Transactions')
    transaction_graph_path = os.path.join(static_dir, 'transactions_by_date.png')
    plt.savefig(transaction_graph_path)
    plt.close()

    # Data for flagged transactions
    flagged_counts = Transaction.objects.filter(flagged=True).values('date__date').annotate(count=Count('id')).order_by('date__date')
    flagged_dates = [entry['date__date'] for entry in flagged_counts]
    flagged_count = [entry['count'] for entry in flagged_counts]

    # Create flagged transaction graph
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=flagged_dates, y=flagged_count, marker='o', color='red')
    plt.title('Flagged Transactions by Date')
    plt.xlabel('Date')
    plt.ylabel('Number of Flagged Transactions')
    flagged_graph_path = os.path.join(static_dir, 'flagged_transactions_by_date.png')
    plt.savefig(flagged_graph_path)
    plt.close()

    # Data for fraud alerts
    fraud_alerts = FraudAlert.objects.values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')
    alert_dates = [entry['created_at__date'] for entry in fraud_alerts]
    alert_counts = [entry['count'] for entry in fraud_alerts]

    # Create fraud alert graph
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=alert_dates, y=alert_counts, marker='o', color='purple')
    plt.title('Fraud Alerts by Date')
    plt.xlabel('Date')
    plt.ylabel('Number of Alerts')
    alert_graph_path = os.path.join(static_dir, 'fraud_alerts_by_date.png')
    plt.savefig(alert_graph_path)
    plt.close()

    # Return paths to the saved graphs
    return {
        'transaction_graph': '/static/graphs/transactions_by_date.png',
        'flagged_graph': '/static/graphs/flagged_transactions_by_date.png',
        'alert_graph': '/static/graphs/fraud_alerts_by_date.png',
    }

def transaction_dashboard(request):
    graph_paths = generate_graphs()
    return render(request, 'dashboard/dashboard.html', {'graph_paths': graph_paths})
