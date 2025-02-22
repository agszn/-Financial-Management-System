from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns = [
    path('', views.base, name='base'),
    
    path('register/', views.register, name='register'),
    path('confirm_otp/', views.confirm_otp, name='confirm_otp'),
    path('login/', views.login_with_otp, name='login'),
    path('confirm_login_otp/', views.confirm_login_otp, name='confirm_login_otp'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    

    path('profile/', views.profile_view, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

        # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # expense
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/update/<int:id>/', views.expense_update, name='expense_update'),
    path('expenses/delete/<int:id>/', views.expense_delete, name='expense_delete'),

    # Income URLs
    path('incomes/', views.income_list, name='income_list'),
    path('incomes/create/', views.income_create, name='income_create'),
    path('incomes/<int:pk>/update/', views.income_update, name='income_update'),
    path('incomes/<int:pk>/delete/', views.income_delete, name='income_delete'),

    # Bill URLs
    path('bills/', views.bill_list, name='bill_list'), 
    path('bill/add/', views.bill_form, name='bill_form'),  
    path('bill/edit/<int:bill_id>/', views.bill_form, name='bill_form'), 

    path('budget/', views.manage_budget, name='manage_budget'),
    path('index/', views.index, name='index'),
    
    # transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/update/<int:pk>/', views.transaction_update, name='transaction_update'),
    path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    path('transactions/view/', views.view_transactions, name='view_transactions'),
    path('transaction/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    
    # fraud
    path('transactions/flag/<int:transaction_id>/', views.flag_transaction, name='flag_transaction'),
    path('admin/blacklist/<str:credit_card_number>/', views.blacklist_credit_card, name='blacklist_credit_card'),

    
    # admin
    path('alert/', views.alert, name='alert'),
    path('notifications/', views.admin_notifications, name='admin_notifications'),
    path('fraud-alerts/', views.fraud_alerts, name='fraud_alerts'),
    path('blacklisted-credit_card_number/', views.blacklisted_credit_card_number, name='blacklisted_credit_card_number'),


    path('dashboardA/', views.transaction_dashboard, name='dashboardA'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

