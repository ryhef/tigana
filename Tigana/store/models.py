from datetime import date

from django.db import models
from django.core.mail import send_mail

from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html



# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    item_text = models.TextField(max_length=200)
    item_qty = models.IntegerField(default=0)
    item_price = models.DecimalField(default=0.0,max_digits=7, decimal_places=2)

    def sale(self, qty):
        self.item_qty = self.item_qty - qty
    def cancel(self, qty):
        self.item_qty = self.item_qty + qty
    def __str__(self):
        return self.item_name

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to='website\static\website\images', height_field=None, width_field=None, max_length=100)
    def __str__(self):
        return self.image_name


class Inquiry(models.Model):
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=50)
    date_of_inquiry = models.DateTimeField(default=timezone.now)
    question = models.TextField()
    PHONE = 'Phone'
    EMAIL = 'Email'
    CONTACT_METHOD = [(PHONE,'Phone'),(EMAIL,'Email')]
    prefered_contact_method = models.CharField(max_length=5, choices=CONTACT_METHOD)
    RECIEVED = 'Received'
    ONGOING = 'Ongoing'
    REPLIED = 'Replied'
    CLOSED = 'Closed'
    INQUIRY_STATUS = [(RECIEVED,'Received'),(REPLIED, 'Replied'),(ONGOING, 'Ongoing'),(CLOSED,'Closed')]
    status = models.CharField(max_length=8, choices=INQUIRY_STATUS,)
    reminder_flag = models.BooleanField(default = False)
    reminder = models.DateField(default=date.today)
    reminder_notes = models.TextField(default="No reminder")
    def __str__(self):
        return self.customer_last_name
    def inquiry_received_email(self):
        msg = 'Your inquiry has been received and we will contact you !\n '
        send_mail(
            'Tigana - Inquiry Received',
            msg,
            None,
            [self.customer_email,''],
            fail_silently=False,
        )

    @admin.display(
        description='reminder due',
    )
    def reminder_due(self):
        due = self.reminder >= date.today()
    
        if(self.reminder_flag == False):
            return "No Reminder"
        else:
            if(due):
                if(self.reminder == date.today()):
                    return format_html('<span style="color: #FFFF00;">DUE TODAY</span>',)
                else:
                    return self.reminder
            else:
                return format_html('<span style="color: #FF0000;">PAST DUE</span>',)

