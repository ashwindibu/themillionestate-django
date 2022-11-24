from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('propertys', views.propertys, name="propertys"),
    path('suggestionapi', views.suggestionapi, name="suggestionapi"),
    path('propertys/<slug:category_slug>/', views.propertys, name="property_by_category"),
    path('property-single/<str:pk>/', views.property_single, name="property_single"),

 ]