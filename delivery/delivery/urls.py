"""delivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include,url
from restaurant import views
from rest_framework.routers import DefaultRouter
from api import views as api_views

router = DefaultRouter()
router.register(r'restaurants', api_views.RestaurantViewset)
router.register(r'menus', api_views.MenuViewset)

urlpatterns = [
    path('', views.IndexView.as_view()),
    url('^api/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurant.urls')),
    path('api/menus/restaurant/<restaurant>', api_views.RestaurantMenuList().as_view()),
    path('api/menus/restaurant/<restaurant>/categories', views.get_restaurant_food_categories),    
]

if settings.DEBUG:    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)