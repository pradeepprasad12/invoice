# in yourappname/admin.py

from django.contrib import admin
from .models import Invoice, InvoiceDetail
from django import forms

class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceDetailInline, ]
    list_display = ('id', 'date', 'customer_name')
    search_fields = ('customer_name', )
    

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the Invoice field queryset to display customer names
        self.fields['invoice'].queryset = Invoice.objects.all()
        self.fields['invoice'].label_from_instance = lambda obj: f"{obj.customer_name} (Invoice {obj.id})"

class InvoiceDetailAdmin(admin.ModelAdmin):
    form = InvoiceDetailForm
    list_display = ('id', 'get_customer_name', 'description', 'quantity', 'unit_price', 'price')
    search_fields = ('invoice__customer_name', 'description', )

    def get_customer_name(self, obj):
        return obj.invoice.customer_name

    get_customer_name.short_description = 'Customer Name'
    get_customer_name.admin_order_field = 'invoice__customer_name'
    
    
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)


