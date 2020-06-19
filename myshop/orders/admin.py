from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

import csv
import datetime

from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):

    model = OrderItem
    raw_id_fields = ['product']

# Custom admin action to export Orders to csv file.
def export_to_csv(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={}.csv'.format(opts.verbose_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)
    # Get model fields, excluding many-to-many and one-to-many relationships
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Write first row with header
    writer.writerow([field.verbose_name for field in fields])

    # write data to rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/$m/%Y')

            data_row.append(value)

        writer.writerow(data_row)

    return response
export_to_csv.short_description = 'Export to CSV'

# Returns an HTML link for the admin_order_detail url to link to specific orders in admin page.
def order_detail(obj):

    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):

    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'first_name', 'last_name', 'address',
                    'postal_code', 'city', 'paid',
                    'created', 'updated',
                    order_detail,
                    order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]

    actions = [export_to_csv]

