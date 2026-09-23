from django.urls import path
from .views import payment_page, transaction_history, refund_payment, webhook, dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("", payment_page, name="payment_page"),
    path("history/", transaction_history, name="transaction_history"),
    path("refund/<str:transaction_id>/", refund_payment, name="refund_payment"),
    path("webhook/", webhook, name="webhook"),
    path("dashboard/", dashboard, name="dashboard"),
]