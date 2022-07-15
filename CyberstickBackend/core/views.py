from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from .serializer import *
from .models import *
from core.forms import CyberstickAdminAuthenticationForm
from django.contrib.auth.views import LoginView
import functools
import json

class CyberstickLoginView(LoginView):
    form_class = CyberstickAdminAuthenticationForm

class ProductView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = [{'id': obj.id, 'color': obj.color, 'price': obj.price} 
        for obj in Product.objects.all()]
        return Response(products)

class CustormerView(APIView):
    serializer_class = CustomerSerializer

    def get(self, request):
        customers = [{'first_name': obj.first_name, 'last_name': obj.last_name,
        'street_address': obj.street_address, 'country': obj.country,
        'zip_code': obj.zip_code, 'city_state': obj.city_state,
        'email': obj.email, 'phone_number': obj.phone_number} for obj in Customer.objects.all()]
        return Response(customers)
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        order = Order.objects.get(id=request.data['order_id'])
        if serializer.is_valid(raise_exception=True):
            customer = serializer.save()
            order.customer = customer
            order.save()
            return Response(serializer.data)

class OrderListView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        orders = [{'customer first name': obj.customer.first_name if obj.customer else None,
        'customer last name': obj.customer.last_name if obj.customer else None,
        'product': obj.item.name,
        'amount': obj.amount, 
        'color': obj.color, 'total price': obj.total_price, 'date': obj.date.__str__(),
        'status': obj.status} for obj in Order.objects.order_by('-date')]
        return Response(orders)

    def post(self, request):    
        serializer = OrderSerializer(data=request.data)
        id = request.data.get('product_id') if request.data.get('product_id') else 1
        product = Product.objects.get(id=id)
        if serializer.is_valid(raise_exception=True):
            total_price = float(serializer.validated_data['total_price'])
            serializer.save(total_price='{:2f}'.format(total_price),
            item=product)
            product.inventory -= serializer.validated_data['amount'];
            product.save()
            return Response(serializer.data)

class SingleOrderView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = SingleOrderSerializer


days_str = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
days_int = dict([(value, key) for key, value in days_str.items()])

class CustomDashboardView(View):
    def get(self, request, *args, **kwargs):
        """Admin dashboard logics and analytics"""
        test_cost = 10000
        month = int(request.GET.get('month')) if int(request.GET.get('month')) > 0 else timezone.now().month

        today_from = timezone.now() - timedelta(days=1)
        yesterday_from = timezone.now() - timedelta(days=2)
        todays_orders = Order.objects.filter(~Q(status=1), date__gte=today_from)
        yesterdays_orders = Order.objects.filter(~Q(status=1), date__range=[yesterday_from, today_from])
        today_revenue = functools.reduce(lambda a, b: a+b, [order.total_price for order in todays_orders]) if todays_orders else 0
        yesterday_revenue = functools.reduce(lambda a, 
        b: a+b, [order.total_price for order in yesterdays_orders]) if yesterdays_orders else 0
        daily_per_diff_rev = ((today_revenue - yesterday_revenue) / 100)

        day = days_str[timezone.now().ctime()[:3]]
        days_earnings = {}
        counter = 1
        
        while day > 0: # get revenues for each day in current week
            start = timezone.now() - timedelta(days=day)
            end = timezone.now() - timedelta(days=day-1)
            day_orders = Order.objects.filter(~Q(status=1), date__range=[start, end])
            day_revenue = functools.reduce(lambda a, b: a+b, [order.total_price for order in day_orders]) if day_orders else 0
            day_earning = day_revenue - (test_cost * day_orders.count())
            days_earnings[days_int[counter]] = float(day_earning)
            counter += 1
            day -= 1

        week_sales = {}
        new_date = date.today()
        year, week_num, day_of_week = new_date.isocalendar()
        v1_week_orders = Order.objects.filter(~Q(status=1), Q(item__id=1), Q(date__week=week_num))
        hdwebcam_week_orders = Order.objects.filter(~Q(status=1), Q(item__id=2), Q(date__week=week_num))
        remote_week_orders = Order.objects.filter(~Q(status=1), Q(item__id=3), Q(date__week=week_num))
        v2_week_orders = Order.objects.filter(~Q(status=1), Q(item__id=4), Q(date__week=week_num))
        v1_sale = functools.reduce(lambda a, b: a+b, [order.total_price for order in v1_week_orders]) if v1_week_orders else 0
        hdwebcam_sale = functools.reduce(lambda a, b: a+b, [order.total_price for order in hdwebcam_week_orders]) if hdwebcam_week_orders else 0
        remote_sale = functools.reduce(lambda a, b: a+b, [order.total_price for order in remote_week_orders]) if remote_week_orders else 0
        v2_sale = functools.reduce(lambda a, b: a+b, [order.total_price for order in v2_week_orders]) if v2_week_orders else 0

        week_sales['1'] = float(v1_sale)
        week_sales['2'] = float(hdwebcam_sale)
        week_sales['3'] = float(remote_sale)
        week_sales['4'] = float(v2_sale)

        month_orders = Order.objects.filter(~Q(status=1), Q(date__month=month))
        last_month_orders = Order.objects.filter(~Q(status=1), Q(date__month=month-1))
        month_per_diff_order = ((len(month_orders) - len(last_month_orders)) / 100)

        total_revenue = functools.reduce(lambda a, b: a+b, [order.total_price for order in month_orders]) if month_orders else 0
        last_total_revenue = functools.reduce(lambda a, b: a+b, [order.total_price for order in last_month_orders]) if last_month_orders else 0
        month_per_diff_rev = ((total_revenue - last_total_revenue) / 100)

        this_month_visitors = Customer.objects.filter(date__month=month).values('email').distinct()
        last_month_visitors = Customer.objects.filter(date__month=month-1).values('email').distinct()
        month_per_diff_vis = ((len(this_month_visitors) - len(last_month_visitors)) / 100)
        
        context = {
                'month': month,    
                'products_sold': len(month_orders),
                'visitors': len(this_month_visitors),
                'today_revenue': today_revenue,
                'daily_per_diff_rev': daily_per_diff_rev,
                'month_per_diff_vis': month_per_diff_vis,
                'month_per_diff_order': month_per_diff_order,
                'month_per_diff_rev': month_per_diff_rev,
                'total_revenue': total_revenue,
                'days_earnings': json.dumps(days_earnings),
                'week_sales': json.dumps(week_sales),
                'recent_orders': Order.objects.exclude(status=1).order_by('-date')[:3],
            }    
        return render(request, 'admin/custom_dashboard.html', context)

class CustomSettingsView(View):
    def get(self, request):
        context = {}
        return render(request, 'admin/custom_settings.html', context)
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        if (request.POST.get('first_name')):
            user.first_name = request.POST['first_name']
        if (request.POST.get('last_name')):
            user.last_name = request.POST['last_name']    
        if (request.POST.get('email')):
            user.email = request.POST['email']
        if (request.POST.get('phone')):
            user.phone_number = request.POST['phone']
        if (request.POST.get('address')):
            user.address = request.POST['address']
        if (request.FILES.get('image')):
            user.image = request.FILES['image']
        user.save()
        return redirect('/cyberstickadmin/')
