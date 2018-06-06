from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from restaurant.models import Restaurant, FoodCategory, Menu

# Create your views here.
class IndexView(TemplateView):
    template_name = 'restaurant/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['restaurant_count'] = Restaurant.objects.count()
        context['food_categories'] = FoodCategory.objects.all()
        context['restaurants'] = Restaurant.objects.all()
        context['top_meals'] = Menu.objects.filter().order_by('-likes')[:3]
        return context