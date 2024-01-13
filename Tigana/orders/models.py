from email.policy import default
from django.db import models

from django.utils import timezone

from store.models import Item
from django.core.mail import send_mail, send_mass_mail

# Create your models here.



class Order(models.Model):
    customer_first_name  = models.CharField(max_length=50)
    customer_last_name  = models.CharField(max_length=50)
    customer_email  = models.EmailField()
    customer_phone  = models.CharField(max_length=50)
    date_of_order = models.DateTimeField(default=timezone.now)
    RECEIVED = 'Received'
    DEPOSIT = 'Deposit'
    PAID = 'Paid'
    CANCELLED = 'Cancelled'
    COMPLETE = 'Complete'
    ORDER_STATUS = [(RECEIVED,'Received'),(DEPOSIT,'Deposit'),(PAID,'Paid'),(COMPLETE,'Complete'),(CANCELLED,'Cancelled')]
    status = models.CharField(max_length=9, choices=ORDER_STATUS, default=RECEIVED)

    CASH = 'Cash'
    EMAIL= 'Email Transfer'
    PAYMENT_TYPE = [(EMAIL,'Email Transfer'),(CASH,'Cash')]
    payment_method = models.CharField(max_length=14, choices=PAYMENT_TYPE, default=EMAIL)

    def __str__(self):
        return str(self.pk)  
    def order_total(self):
        sum = 0
        orderlines = LineItem.objects.filter(orderNumber=self.pk)
        for orderline in orderlines:
            sum = sum + orderline.line_total()
        return sum
    def order_received_email(self):
        subject ='Hiddenview Hereford - Order #' + str(self.pk) 
        msg = 'Order#' + str(self.pk)  +' has been received.\n' + 'Payment Instructions\n' + 'Pick up instructions\n'
        send_mail(
            subject,
            msg,
            None,
            [self.customer_email,'hiddenviewproject@outlook.com'],
            fail_silently=False,
        )      


class LineItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    line_number = models.PositiveIntegerField(default=0)
    orderNumber = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    def __str__(self):
        return str(self.pk) 
    def line_total(self):
        return self.qty * self.item.item_price

