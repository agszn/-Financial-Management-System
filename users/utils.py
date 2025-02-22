from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list, from_email=None):
    """
    Sends an email using Django's email backend.
    
    Args:
        subject (str): Subject of the email.
        message (str): Body of the email.
        recipient_list (list): List of recipient email addresses.
        from_email (str): Sender's email address (default: settings.DEFAULT_FROM_EMAIL).
        
    Returns:
        int: Number of successfully delivered messages.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    return send_mail(subject, message, from_email, recipient_list)

from django.core.mail import send_mail
from django.utils.timezone import now
from .models import BillPayment
from datetime import timedelta, date

def send_reminder_notifications():
    today = date.today()
    bills = BillPayment.objects.filter(paid=False).exclude(reminder_type='none')

    for bill in bills:
        # Determine if a reminder is due
        if bill.reminder_type == 'weekly' and (today - bill.due_date).days % 7 == 0:
            send_email_reminder(bill)
        elif bill.reminder_type == 'monthly' and today.day == bill.due_date.day:
            send_email_reminder(bill)
        elif bill.reminder_type == 'specific_date' and bill.reminder_date == today:
            send_email_reminder(bill)

def send_email_reminder(bill):
    subject = f"Reminder: Payment Due for {bill.bill_name}"
    message = (
        f"Dear User,\n\n"
        f"This is a reminder that your payment for '{bill.bill_name}' "
        f"amounting to ₹{bill.amount} is due on {bill.due_date}.\n\n"
        f"Please ensure timely payment to avoid penalties.\n\n"
        f"Best regards,\nYour Budget Manager"
    )
    recipient_list = [bill.user.email]  # Assuming you associate `user` with bills
    send_mail(subject, message, 'shreyasankapal24@gmail.com', recipient_list)


from django.core.mail import send_mail
from django.conf import settings

def send_email(to_email, subject, message):
    """
    Helper function to send email using Django's built-in email backend.
    """
    from_email = settings.EMAIL_HOST_USER  # Using the email configured in settings

    # Ensure 'to_email' is passed as a list
    recipient_list = [to_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
