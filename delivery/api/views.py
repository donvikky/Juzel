from rest_framework import viewsets
from rest_framework import generics
from restaurant.models import Restaurant, Menu
from api.serializers import RestaurantSerializer, MenuSerializer, RestaurantFoodCategorySerializer

# Create your views here.
class RestaurantViewset(viewsets.ModelViewSet):
    """
    This viewset automatically provides a list of restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
class MenuViewset(viewsets.ModelViewSet):
    """
    This viewset automatically provides a list of menus
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class RestaurantMenuList(generics.ListAPIView):
    """
    This viewset automatically provides a list of menus belonging to a restaurant
    """
    serializer_class = MenuSerializer

    def get_queryset(self):
        """
        Filters the menu table for a specific restaurant's menus
        """
        restaurant = self.kwargs['restaurant']
        return Menu.objects.filter(restaurant=restaurant)


class RestaurantFoodCategoryList(generics.ListAPIView):
    
    serializer_class = RestaurantFoodCategorySerializer

    def get_queryset(self):
        
        restaurant = self.kwargs['restaurant']
        r = Restaurant.objects.filter(pk=restaurant)
        return r
    
