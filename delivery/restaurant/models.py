from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class State(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    name = models.CharField(max_length=250)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class Lga(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    state = models.ForeignKey(State,related_name='lgas', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class Town(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    state = models.ForeignKey(State,related_name='towns', on_delete=models.CASCADE)
    lga = models.ForeignKey(Lga,related_name='lga_towns', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class FoodCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Food Categories'

class Food(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey(FoodCategory, related_name='category', on_delete=models.CASCADE,
                default=None)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='foods', on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='user_foods', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RestaurantCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Restaurant Categories'

class Restaurant(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    state = models.ForeignKey(State, related_name='restaurants', on_delete=models.CASCADE)
    lga = models.ForeignKey(Lga,related_name='restaurants', on_delete=models.CASCADE)
    town = models.ForeignKey(Town,related_name='restaurant_town',null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    address = models.TextField()    
    primary_phone = models.BigIntegerField()
    secondary_phone = models.BigIntegerField(blank=True,null=True)
    email = models.EmailField(max_length=250)
    website = models.URLField(blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    logo = models.ImageField()
    latitude = models.DecimalField(blank=True, null=True,max_digits=15,decimal_places=9)
    longitude = models.DecimalField(blank=True, null=True,max_digits=15,decimal_places=9)
    categories = models.ManyToManyField(RestaurantCategory)
    food_categories = models.ManyToManyField(FoodCategory)
    likes = models.PositiveIntegerField(default=0)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='user_restaurants',on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='restaurants', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Menu(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_offering', on_delete=models.CASCADE)
    food = models.ForeignKey(Food,related_name='food_offerings', on_delete=models.CASCADE)    
    price = models.DecimalField(max_digits=8,decimal_places=2)
    image = models.ImageField()
    description = models.TextField(null=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    likes = models.PositiveIntegerField(default=0)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='food_offering_creater', on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='food_offering_updater', on_delete=models.CASCADE)

    def __str__(self):
        return self.food.name

    class Meta:
        unique_together = ('food', 'restaurant',)

    def food_name(self):
        return self.food.name

    def restaurant_address(self):
        return self.restaurant.address

    def restaurant_state(self):
        return self.restaurant.state.name    
    
    def restaurant_logo(self):
        return str(self.restaurant.logo)

    def menu_image(self):
        return str(self.image)

    def food_category(self):
        return self.food.category

