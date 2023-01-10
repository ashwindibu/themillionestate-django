from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name="home"),
    # path('user-signup',views.user_signup, name="user_signup"),
    path('user-login', views.user_login, name="user_login"),
    path('user-logout',views.user_logout, name="user_logout"),
    path('contact', views.contact, name="contact"),
    path('propertys', views.propertys, name="propertys"),
    path('suggestionapi', views.suggestionapi, name="suggestionapi"),
    path('propertys/<slug:category_slug>/', views.propertys, name="property_by_category"),
    path('property-single/<str:pk>/', views.property_single, name="property_single"),
    path('user-profile', views.user_profile, name="user_profile"),
    path('my-property', views.my_property, name="my_property"),
    path('favourite-property', views.favourite_property, name="favourite_property"),
    path('add-property', views.add_property, name="add_property"),
    path('user-register', views.user_register, name="user_register"),
    path('my_property_edit/<str:pk>/', views.my_property_edit, name="my-property-edit"),
    path('my_property_delete/<str:pk>/', views.my_property_delete, name="my-property-delete"),
    # path('accounts/login/', views.user_login, name="account_login")

 ]