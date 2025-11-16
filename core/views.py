from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from users.models import CustomUser
from orders.models import Order, Customer


class IndexView(TemplateView):
    """
    Main landing page view showing dashboard with users and orders statistics
    """
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get recent users
        context['recent_users'] = CustomUser.objects.all().order_by('-date_joined')[:8]
        context['total_users'] = CustomUser.objects.count()
        
        # Get orders statistics
        context['total_orders'] = Order.objects.count()
        context['new_orders'] = Order.objects.filter(status=Order.StatusChoice.NEW).count()
        context['completed_orders'] = Order.objects.filter(status=Order.StatusChoice.COMPLETED).count()
        
        # Get recent orders
        context['recent_orders'] = Order.objects.select_related('customer__user').order_by('-registered_at')[:5]
        
        # Calculate total revenue
        context['total_revenue'] = Order.objects.filter(
            status=Order.StatusChoice.COMPLETED
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Get weekly stats for chart
        last_7_days = timezone.now() - timedelta(days=7)
        context['weekly_orders'] = Order.objects.filter(
            registered_at__gte=last_7_days
        ).extra(
            select={'day': 'DATE(registered_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        return context
