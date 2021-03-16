import csv
import datetime

from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import OrderItem, Order


def export_to_csv(modeladmin, request, queryset):
    """ A custom action to generate a csv file from an order object. """
    opts = modeladmin.model._meta
    print(opts)
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    # get fields of the model, excluding one-to-many and many-to-many relationships.
    fields = [field for field in opts.get_fields() if
              not field.many_to_many and
              not field.one_to_many]

    # first row with header information.
    writer.writerow([field.verbose_name for field in fields])
    # write data per row
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    """ Admin item. Link to view order detail. """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    """ Admin item. Link to view order detail as pdf. """
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated',
                    order_detail, order_pdf]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
