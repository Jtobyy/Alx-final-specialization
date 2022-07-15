from django.db.models import Q
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *
import functools
from django.utils.safestring import mark_safe

class CyberstickAdminSite(admin.AdminSite):
    site_header = "Cyberstick"
    site_title = "Cyberstick Admin Portal"
    index_title = ""

    def get_app_list(self, request):
        ordering = {
            "Orders": 1,
            "Products": 2,
            "Customers": 3,
        }            
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        for app in app_list:
            app["models"].sort(key=lambda x: ordering[x["name"]])
        return app_list

cyberstick_site = CyberstickAdminSite(name='CyberstickAdmin')

class ProductAdmin(admin.ModelAdmin):
    def product_pic(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
        url = obj.headshot.url,
        width=obj.headshot.width,
        height=obj.headshot.height,
        )
        )    

    def stock(self, obj):
        if obj.inventory > 0:    
            return 'In stock'
        else:
            return 'Out of stock'    
    def product_id(self, obj):
        return obj.id
    list_display = ('name', 'stock', 'price', 'product_id', 'tags', 'date')
    readonly_fields = ('product_pic', )

cyberstick_site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):    
    list_per_page = 20
    list_display = ('id', 'get_group_id', 'product_name', 'customer_name', 'total_price', 'status')
    list_display_links = ('get_group_id',)

    def product_name(self, obj):
        queryset = Order.objects.filter(Q(group_id=obj.id) | Q(id=obj.id))
        return ", ".join([
            child.item.name for child in queryset
        ])
    product_name.short_description = "Product (s)"
    def product_image(self, obj):
        return obj.item.image
    def product_price(self, obj):   
        return obj.item.price
    def customer_name(self, obj):
        return obj.customer.first_name + ' ' + obj.customer.last_name
    def customer_email(self, obj):
        return obj.customer.email
    def customer_phone(self, obj):
        return obj.customer.phone_number
    def customer_city(self, obj):
        return obj.customer.city_state
    def customer_address(self, obj):
        return obj.customer.street_address
    def customer_zipcode(self, obj):
        return obj.customer.zip_code
    def get_status(self, obj):
        return obj.get_status_display()
    def get_group_id(self, obj):
        if not obj.group_id:
            return obj.id
        return False
    get_group_id.short_description = "serial number"        
    
    def has_add_permission(self, request, obj=None):
        return False    
    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        custom_queryset = queryset.filter(group_id=None)
        return custom_queryset

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}    
        try:    
            queryset = Order.objects.filter(Q(group_id=object_id) | Q(id=object_id))
            orders_total = functools.reduce(lambda a, b: a+b, [order.total_price for order in queryset]) if queryset else 0
            orders_details = [{"product": obj.item,
            "quantity": obj.amount, "unit_price": float(obj.item.price), "total": float(obj.total_price),
            } for obj in queryset]
            orders_details.append(orders_total)
            extra_context['linked_orders'] = orders_details
            '''
            serializer = AdminLinkedOrdersSerializer(orders_details, many=True)
            json = JSONRenderer().render(serializer.data)
            return Response(json, content_type='application/json')
            '''
        except Exception as e:
            print(e)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)   
                
    def get_readonly_fields(self, request, obj=None):
        if obj:    
            fields = ('id', 'group_id', 'customer', 'customer_email', 'customer_phone',
            'item', 'amount', 'color', 'total_price', 'payment_method', 'get_status', 'customer_city',
            'customer_address', 'customer_zipcode', 'product_image', 'product_price', 'total_price',
            )
            return fields
        else:
            return []

    def save_model(self, request, obj, form, change):    
        related = Order.objects.filter(Q(group_id=obj.id))
        for object in related:
            object.status = obj.status
            object.save()
            print(object)
        super().save_model(request, obj, form, change)
        
    #list_editable = ('total_price', 'status')
    #search_fields=('status',)
cyberstick_site.register(Order, OrderAdmin)

class CustomerAdmin(admin.ModelAdmin):    
    list_display = ('name', 'email', 'orders', 'date')    

    def name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    def orders(self, obj):
        return list(obj.order_set.all())

    def has_add_permission(self, request):
        return False
cyberstick_site.register(Customer, CustomerAdmin)
#cyberstick_site.register(User)

