from django.contrib import admin
from .models import PaymentTransaction, Invoice


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):

    list_display = (
        'transaction_id',
        'customer_name',
        'amount',
        'payment_method',
        'status',
        'created_at',
    )

    list_filter = (
        'payment_method',
        'status',
    )

    search_fields = (
        'transaction_id',
        'customer_name',
        'customer_email',
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        'invoice_number',
        'transaction',
        'generated_at',
    )

    search_fields = (
        'invoice_number',
    )