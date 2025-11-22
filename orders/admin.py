from django.contrib import admin
from orders.models import Customer, Order, OrderElement


class OrderElementInline(admin.TabularInline):
    model = OrderElement
    extra = 1
    readonly_fields = ['total_price']
    fields = ['product', 'price', 'quantity', 'total_price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'phone', 'get_orders_count']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['id', 'user']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_orders_count(self, obj):
        return obj.orders.count()
    get_orders_count.short_description = 'Orders'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'status', 'total_price', 'registered_at']
    list_filter = ['status', 'registered_at', 'is_draft']
    search_fields = ['customer__user__username', 'address']
    readonly_fields = ['registered_at', 'id']
    inlines = [OrderElementInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer', 'address', 'order_note')
        }),
        ('Status', {
            'fields': ('status', 'is_draft')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Timeline', {
            'fields': ('registered_at', 'called_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderElement)
class OrderElementAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    list_filter = ['order__status']
    search_fields = ['order__customer__user__username', 'product__name']
    readonly_fields = ['id']
