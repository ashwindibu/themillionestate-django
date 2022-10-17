from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'adminpanel/adminhome.html')

def admin_property_list(request):
    return render(request, 'adminpanel/admin-property-list.html')

def admin_add_property(request):
    return render(request, 'adminpanel/admin-add-property.html')

def admin_property_for(request):
    return render(request, 'adminpanel/admin-property-for.html')

def admin_property_type(request):
    return render(request, 'adminpanel/admin-property-type.html')