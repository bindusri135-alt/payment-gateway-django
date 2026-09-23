from django.db import models


class PaymentTransaction(models.Model):

    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    customer_email = models.EmailField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Payment verification
    payment_verified = models.BooleanField(
        default=False
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.transaction_id


class Invoice(models.Model):

    transaction = models.OneToOneField(
        PaymentTransaction,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number