from django.contrib import admin

from .models import Category, Product, BuyPrice, Order


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ['User information', {
            'fields': ('sell_user', 'name', 'descp', 'img', 'sell_begin', 'sell_end', 'status', 'price', 'category'),
        }],
    )

    list_display = ('id', 'name', 'sell_begin', 'sell_end', 'status', 'price')
    list_filter = ['status']
    list_editable = ["status"]
    search_fields = ['name']


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
