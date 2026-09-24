
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import PaymentTransaction, Invoice
from reportlab.pdfgen import canvas
import uuid


@login_required
def payment_page(request):

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        customer_email = request.POST.get("customer_email")
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")

        transaction = PaymentTransaction.objects.create(
            transaction_id=str(uuid.uuid4())[:12],
            customer_name=customer_name,
            customer_email=customer_email,
            amount=amount,
            payment_method=payment_method,
            status="success",
            payment_verified=True,
            verified_at=timezone.now()
        )

        # Create invoice automatically
        invoice = Invoice.objects.create(
            transaction=transaction,
            invoice_number="INV-" + transaction.transaction_id
        )

        return render(request, "success.html", {
            "transaction": transaction,
            "invoice": invoice
        })

    return render(request, "payment.html")


def transaction_history(request):

    transactions = PaymentTransaction.objects.all().order_by("-created_at")

    return render(request, "history.html", {
        "transactions": transactions
    })


def refund_payment(request, transaction_id):

    transaction = get_object_or_404(
        PaymentTransaction,
        transaction_id=transaction_id
    )

    if request.method == "POST":

        transaction.status = "refunded"
        transaction.save()

        return render(request, "refund_success.html", {
            "transaction": transaction
        })

    return render(request, "refund.html", {
        "transaction": transaction
    })


def webhook(request):

    if request.method == "POST":

        data = request.body

        print("Webhook received:", data)

        return JsonResponse({
            "status": "success",
            "message": "Webhook received successfully"
        })

    return JsonResponse({
        "message": "Webhook endpoint is active"
    })


def dashboard(request):

    transactions = PaymentTransaction.objects.all()

    total_transactions = transactions.count()

    successful_payments = transactions.filter(
        status="success"
    ).count()

    refunded_payments = transactions.filter(
        status="refunded"
    ).count()

    total_amount = sum(
        transaction.amount
        for transaction in transactions
        if transaction.status == "success"
    )

    return render(request, "dashboard.html", {
        "total_transactions": total_transactions,
        "successful_payments": successful_payments,
        "refunded_payments": refunded_payments,
        "total_amount": total_amount,
    })


def invoice_pdf(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    transaction = invoice.transaction

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{invoice.invoice_number}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 780, "PAYMENT INVOICE")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        80, 730,
        f"Invoice Number: {invoice.invoice_number}"
    )

    pdf.drawString(
        80, 700,
        f"Transaction ID: {transaction.transaction_id}"
    )

    pdf.drawString(
        80, 670,
        f"Customer: {transaction.customer_name}"
    )

    pdf.drawString(
        80, 640,
        f"Email: {transaction.customer_email}"
    )

    pdf.drawString(
        80, 610,
        f"Amount: Rs. {transaction.amount}"
    )

    pdf.drawString(
        80, 580,
        f"Payment Method: {transaction.get_payment_method_display()}"
    )

    pdf.drawString(
        80, 550,
        f"Status: {transaction.status}"
    )

    pdf.showPage()
    pdf.save()

    return response

