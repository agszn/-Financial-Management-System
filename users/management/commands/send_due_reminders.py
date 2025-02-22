from django.core.management.base import BaseCommand
from users.models import BillPayment, Notification
from datetime import date
from users.utils import send_email  # Assuming your send_email function is in utils.py

class Command(BaseCommand):
    help = 'Send due reminders for unpaid bills'

    def handle(self, *args, **kwargs):
        # Get all unpaid bills that need reminders
        bills = BillPayment.objects.filter(paid=False)

        for bill in bills:
            if bill.is_reminder_due():
                # Construct email content based on category
                category_messages = {
                    'EMI': f"This is a reminder to pay your EMI for '{bill.bill_name}'.",
                    'Credit Card': f"Reminder: Pay your credit card bill for '{bill.bill_name}'.",
                    'Insurance': f"Insurance payment for '{bill.bill_name}' is due.",
                    'Tax': f"Your tax payment for '{bill.bill_name}' is due.",
                    'General': f"This is a general reminder for your bill '{bill.bill_name}'."
                }
                reminder_message = category_messages.get(bill.reminder_category, "Payment reminder.")

                subject = f"Reminder: {bill.reminder_category} - {bill.bill_name} Due Soon"
                message = (
                    f"Dear User,\n\n"
                    f"{reminder_message}\n\n"
                    f"Amount: ₹{bill.amount}\n"
                    f"Due Date: {bill.due_date}\n\n"
                    f"Please ensure timely payment to avoid penalties.\n\n"
                    f"Thank you."
                )

                user_email = "sznvws@gmail.com"  # Replace with actual user's email
                send_email(user_email, subject, message)

                # Save the notification in the database
                Notification.objects.create(
                    user_email=user_email,
                    title=subject,
                    message=message
                )

                # Update last_reminder_sent
                bill.last_reminder_sent = date.today()
                bill.save()

        self.stdout.write(self.style.SUCCESS('Successfully sent due reminders'))
