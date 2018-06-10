from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:id>/', views.RestaurantMenuView.as_view(), name='menu'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('empty-cart', views.empty_cart, name='empty-cart'),
    path('get-orders', views.get_orders, name='get-orders'),
    path('remove-item/', views.remove_item, name='remove-item'),
]