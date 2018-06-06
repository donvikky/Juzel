from django.contrib import admin
from restaurant.models import (State,Lga,Town, Restaurant, FoodCategory, Food, RestaurantCategory,
            FoodCategory, Menu)

# Register your models here.
class LgaAdmin(admin.ModelAdmin):
    list_display = ('state','name','status')
    list_filter = ('status',)
    search_fields = ['name','state__name']

class RestaurantAdmin(admin.ModelAdmin):
    exclude = ('create_time','create_user','update_time','update_user')
    list_display = ['name','address','town']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user        
        super(RestaurantAdmin, self).save_model(request, obj, form, change)

class FoodAdmin(admin.ModelAdmin):
    exclude = ('create_time','create_user','update_time','update_user')
    list_display = ['name','description','create_time','create_user']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user        
        super(FoodAdmin, self).save_model(request, obj, form, change)

class MenuAdmin(admin.ModelAdmin):
    exclude = ('create_time','create_user','update_time','update_user')
    list_display = ['food','restaurant','price','description']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user        
        super(MenuAdmin, self).save_model(request, obj, form, change)







admin.site.register(State)
admin.site.register(Lga, LgaAdmin)
admin.site.register(Town)
admin.site.register(FoodCategory)
admin.site.register(RestaurantCategory)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Menu, MenuAdmin)