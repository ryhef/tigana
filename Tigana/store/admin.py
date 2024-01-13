from gettext import ngettext
from django.contrib import admin, messages

from .models import Item, ItemImage, Inquiry

#Admin Classes
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name','item_qty','item_price']
    fields = ['item_name','item_text','item_qty','item_price' ]
    inlines = [ItemImageInline]



class InquiryAdmin(admin.ModelAdmin):
    list_display = ['customer_last_name','customer_first_name', 'prefered_contact_method','date_of_inquiry','status','reminder_due']
    list_filter = ['date_of_inquiry','status']
    search_fields = ['customer_last_name','customer_first_name','customer_email']
    actions=['mark_replied']
    @admin.action(description="Mark selected inquiries as replied")
    def mark_replied(self,request,queryset):
        updated = queryset.update(status='Replied')
        self.message_user(request,ngettext(   '%d inquiry was successfully marked as replied.',
            '%d inquiries were successfully marked as replied.',
            updated,
        ) % updated, messages.SUCCESS)

        

# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Inquiry, InquiryAdmin)

