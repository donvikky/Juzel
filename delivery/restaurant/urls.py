from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:id>/', views.RestaurantMenuView.as_view(), name='menu'),
]