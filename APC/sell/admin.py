from django.contrib import admin

from .models import Category, Product, BuyPrice, Order
from .utils import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ['User information', {
            'fields': ('sell_user', 'name', 'detail', 'img', 'sell_begin', 'sell_end', 'status', 'price', 'category'),
        }],
    )

    list_display = ('id', 'name', 'sell_begin', 'sell_end', 'status', 'price')
    list_filter = ['status']
    list_editable = ["status"]
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if obj.sell_begin != "" and obj.sell_begin != None:
                obj.sell_begin_stamp = float(get_stamp_by_time(obj.sell_begin.strftime('%Y-%m-%d %H:%M:%S')))
            if obj.sell_end != "" and obj.sell_end != None:
                obj.sell_end_stamp = float(get_stamp_by_time(obj.sell_end.strftime('%Y-%m-%d %H:%M:%S')))
        super().save_model(request, obj, form, change)


class BuyPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'status', 'price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(BuyPrice, BuyPriceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.site_title = "Auction Personal Collection Management"
admin.site.site_header = "Auction Personal Collection Management"
