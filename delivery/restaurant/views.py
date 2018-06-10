from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from restaurant.models import Restaurant, FoodCategory, Menu, BooleanUtility
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json

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
        context['token'] = Token.objects.get(user_id=1)
        return context


def get_restaurant_food_categories(request, **kwargs):
    """
    This view retrieves all the food categories belonging to a restaurant
    and all the foods belonging to each category
    """
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


@csrf_exempt
def add_to_cart(request):
    """
    This view adds a food item to a cart
    """    
    data = json.loads(request.body)    
    if 'cart' not in request.session:
        # if cart not yet initialized, initialize it then append new item
        request.session['cart'] = []
        request.session['cart'].append(data)
    else:
        BooleanUtility.inside = False
        item_cart = request.session['cart']
        for item in item_cart:
            # if item id exists in session, increase quantity
            if item['id'] == data['id']:
                BooleanUtility.inside = True
                item['qty'] = item['qty'] + 1
                
        request.session['cart'] = item_cart
        if BooleanUtility.inside == False:
            request.session['cart'].append(data)        
    
    request.session.modified = True
    return JsonResponse(data)
    

def empty_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    return JsonResponse({'status':'empty'})


def get_orders(request):
    if 'cart' in request.session:
        data = request.session['cart']
    return JsonResponse(data,safe=False)


@csrf_exempt
def remove_item(request):
    data = json.loads(request.body)
    
    if 'cart' in request.session:        
        item_cart = request.session['cart'] # assign cart session to variable
        for index, item in enumerate(item_cart):
            if item['id'] == data['id']:
                del item_cart[index] # delete selected item
        request.session['cart'] = item_cart # save item_cart back to session       
        request.session.modified = True        
        
    return JsonResponse(data)
    

