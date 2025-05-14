from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'item_price']
    readonly_fields = ['product', 'item_price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'is_paid')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'total_price')

    def save_model(self, request, obj, form, change):
        # Sipariş kaydedildiğinde toplam fiyatı güncelle
        if obj.is_paid:
            total = 0
            for item in obj.items.all():
                total += item.item_price * item.quantity
            obj.total_price = total
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)
