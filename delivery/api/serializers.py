from rest_framework import serializers
from restaurant.models import Restaurant, Menu

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id','name','address','town','logo','latitude','longitude','likes')

class MenuRestaurantNameField(serializers.RelatedField):
    """
    This provides the restaurant's name in the menu serialzier.
    By default the serializer returns the restaurant's ID
    """
    def to_representation(self, value):
        return value.name


class RestaurantLogoField(serializers.RelatedField):
    """
    This provides the restaurant's name in the menu serialzier.
    By default the serializer returns the restaurant's ID
    """
    def to_representation(self, value):
        return value.restaurant.logo

class MenuFoodNameField(serializers.RelatedField):
    """
    This provides the restaurant's name in the menu serialzier.
    By default the serializer returns the restaurant's ID
    """
    def to_representation(self, value):
        return value.name

class MenuSerializer(serializers.ModelSerializer):
    restaurant = MenuRestaurantNameField(read_only=True)

    class Meta:
        model = Menu
        fields = ('id','food_name','price','menu_image','description','likes','restaurant',
       'restaurant_address','restaurant_logo','restaurant_state','restaurant_logo')
    