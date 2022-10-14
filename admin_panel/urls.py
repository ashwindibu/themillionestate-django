from gettext import dgettext
from django.urls import path
from . import views

urlpatterns = [ path('', views.home, name='home'), ]