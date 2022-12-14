from ctypes import alignment
from gettext import dgettext
from django.urls import path
from . import views

urlpatterns = [
    path('admin-login',views.admin_login, name="admin_login"),
    path('', views.home, name='admindashboard'),
    path('adminproperty-list', views.admin_property_list, name='admin-property-lis'),
    path('admin-property-delete/<str:pk>/', views.admin_property_delete, name='admin_property_delete'),
    path('admin-property-add', views.admin_add_property, name='admin_add_property'),
    path('admin-edit-property/<str:pk>/', views.admin_edit_property, name="admin_edit_property"),
    path('admin-property-for', views.admin_property_for, name='admin_property_for'),
    path('admin-property-typ', views.admin_property_type, name='admin_property_type'),
    path('propertytype-add', views.admin_property_type_add, name='property_type_add'),
    path('property_type_delete/<str:pk>/', views.admin_property_type_delete, name="property_type_delete"),
    path('property-for-add',views.property_for_add, name="property_for_add"),
    path('property_for_delete/<str:pk>/',views.property_for_delete, name="property_for_delete"),
    path('admin-location', views.admin_location, name="admin_location"),
    path('admin-country-list',views.admin_country_list, name="admin_country_list"),
    path('country-add', views.country_add, name="country_add"),
    path('country_delete/<str:pk>/', views.country_delete, name="country_delete"),
    path('admin-state-list',views.admin_state_list, name="admin_state_list"),
    path('state-add', views.state_add, name="state_add"),
    path('state-delete/<str:pk>/', views.state_delete, name="state_delete"),
    path('admin-city-list',views.admin_city_list, name="admin_city_list"),
    path('city-add', views.city_add, name="city_add"),
    path('city_delete/<str:pk>', views.city_delete, name="city_delete"),
    path('admin-login',views.admin_login, name="admin_login"),
    path('admin-logout',views.admin_logout, name="admin_logout")
    ]