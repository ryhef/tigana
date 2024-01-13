from django.contrib import admin, messages
from gettext import ngettext

from .models import Order, LineItem

class LineItemInline(admin.TabularInline):
    list_display = ['item','qty','line_total']
    model = LineItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['date_of_order','status']
    list_display = ['__str__','customer_last_name','customer_first_name','status','date_of_order','order_total']
    search_fields = ['customer_last_name']
    inlines = [LineItemInline]
    actions=['cancel_order']
    @admin.action(description="Cancel selected orders")
    def cancel_order(self,request,queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request,ngettext(   '%d inquiry was successfully cancelled.',
            '%d inquiries were successfully marked as replied.',
            updated,
        ) % updated, messages.SUCCESS)

# Register your models here
admin.site.register(Order,OrderAdmin)
