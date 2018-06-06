from rest_framework import viewsets
from restaurant.models import Restaurant, Menu
from api.serializers import RestaurantSerializer, MenuSerializer

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
