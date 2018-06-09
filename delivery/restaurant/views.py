from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from restaurant.models import Restaurant, FoodCategory, Menu
from types import SimpleNamespace

# Create your views here.
class IndexView(TemplateView):
    template_name = 'restaurant/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['restaurant_count'] = Restaurant.objects.count()
        context['food_categories'] = FoodCategory.objects.all()
        context['restaurants'] = Restaurant.objects.all()
        context['top_meals'] = Menu.objects.filter().order_by('-likes')[:3]
        return context


class RestaurantMenuView(TemplateView):
    template_name = 'restaurant/menu.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['id'])
        context['restaurant'] = restaurant
        context['menus'] = Menu.objects.filter(restaurant=restaurant)
        return context


def get_restaurant_food_categories(request, **kwargs):
    restaurant_id = kwargs['restaurant']
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    food_categories = restaurant.food_categories.all()
    
    categories = []
    for category in food_categories:
        d = {}
        d['id'] = category.id
        d['name'] = category.name
        d['foods'] = []
        menus = Menu.objects.filter(restaurant=restaurant_id, food__category=category)
        for menu in menus:
            food = {}
            food['id'] = menu.food.id
            food['name'] = menu.food.name
            food['description'] = menu.description
            food['price'] = menu.price
            food['pic'] = menu.image.url
            food['likes'] = menu.likes
            d['foods'].append(food)
        categories.append(d)
        
    return JsonResponse(categories,safe=False)

