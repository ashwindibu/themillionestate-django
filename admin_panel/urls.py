from gettext import dgettext
from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='admindashboard'),
    path('adminproperty-list', views.admin_property_list, name='admin-property-lis'),
    path('admin-property-add', views.admin_add_property, name='admin_add_property'),
    path('admin-property-for', views.admin_property_for, name='admin_property_for'),
    path('admin-property-type', views.admin_property_type, name='admin_property_type'),
    ]