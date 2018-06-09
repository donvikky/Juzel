from rest_framework import serializers
from restaurant.models import Restaurant, Menu, FoodCategory

class RestaurantFoodCategoryNameField(serializers.RelatedField):
    """
    This provides the restaurant's name in the menu serialzier.
    By default the serializer returns the restaurant's ID
    """
    def to_representation(self, value):
        return value.name

class RestaurantSerializer(serializers.ModelSerializer):
    food_categories = RestaurantFoodCategoryNameField(read_only=True,many=True)
    class Meta:
        model = Restaurant
        fields = ('id','name','address','town','logo','latitude','longitude','likes','food_categories')

class MenuRestaurantNameField(serializers.RelatedField):
    """
    This provides the restaurant's name in the menu serialzier.
    By default the serializer returns the restaurant's ID
    """
    def to_representation(self, value):
        return value.name


class RestaurantLogoField(serializers.RelatedField):
    """
    This provides the restaurant's logo in the menu serialzier.
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

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id','name')
        

class RestaurantFoodCategorySerializer(serializers.ModelSerializer):
    """
    This serializer fetches all the food categories for a restaurant
    """
    food_categories = FoodCategorySerializer
    class Meta:
        model = Restaurant
        fields = ('food_categories',)
    