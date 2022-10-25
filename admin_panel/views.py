from itertools import count
from multiprocessing import context
from urllib.request import HTTPPasswordMgrWithDefaultRealm
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import PropertyTypeForm, PropertyForForm, UserTypeForm, CountryForm, StateForm, CityForm
from property.models import PropertyType, PropertyFor, Property,Country, State, City
from base.models import UserType

# Create your views here.

def home(request):
    return render(request, 'adminpanel/adminhome.html')

def admin_property_list(request):
    return render(request, 'adminpanel/admin-property-list.html')


#PropertyType <---->
def admin_property_type(request):
    property_types = PropertyType.objects.all()
    count = property_types.count()
    context = {
        "data":property_types,
        "count":count
    }
    return render(request, 'adminpanel/admin-property-type.html', context)

def admin_property_type_add(request):
    form = PropertyTypeForm()
    context = {
        'form':form
    }
    if request.method == 'POST':
        form = PropertyTypeForm(request.POST, request.FILES)
        
        print('Going to vaildate')
        if form.is_valid():
            print('Validated complete')
            data = PropertyType()
            data.property_type_name     = form.cleaned_data['property_type_name']
            data.description            = form.cleaned_data['description']
            data.property_type_image    = form.cleaned_data['property_type_image']
            raw_slug                    = form.cleaned_data['property_type_name']
            raw_slug                    = raw_slug.lower()
            slug                        =  "-".join(raw_slug.split())
            imagez                      = form.cleaned_data['property_type_image']
            print(imagez)
            print(slug)
            data.slug                   = slug
            data.save()
            messages.success(request,'Succesfully Added' )
            return render(request, 'adminpanel/admin-property-type-add.html', context)
        else:
            messages.error(request,'Name is already in use.' )
            return redirect(admin_property_type_add)

    return render(request, 'adminpanel/admin-property-type-add.html', context)

def admin_property_type_delete(request, pk):
    PropertyType.objects.filter(id=int(pk)).delete()
    return redirect(admin_property_type)



#PropertyFor <---->
def admin_property_for(request):
    property_for = PropertyFor.objects.all()
    return render(request, 'adminpanel/admin-property-for.html',{"data":property_for})

def property_for_add(request):
    form = PropertyForForm()
    context = {
        "form":form
    }
    if request.method == "POST":
        form = PropertyForForm(request.POST)
        if form.is_valid():
            data = PropertyFor()
            data.property_for_name  = form.cleaned_data['property_for_name']
            raw_slug    = form.cleaned_data['property_for_name']
            raw_slug    = raw_slug.lower()
            slug        = '-'.join(raw_slug.split())
            data.slug   =  slug
            data.save()
            messages.success(request,'Succesfully Added' )
            return render(request, 'adminpanel/admin-property-for-add.html', context)
        else:
            messages.error(request,'Name is already in use.' )
            return redirect(property_for_add)
    return render(request, 'adminpanel/admin-property-for-add.html', context)

def property_for_delete(request,pk):
    PropertyFor.objects.filter(id=int(pk)).delete()
    return redirect(admin_property_for)



#UserType <---->
def user_type(request):
    user_type = UserType.objects.all()
    return render(request, "adminpanel/admin-user-type.html", {'data':user_type })

def user_type_add(request):
    form = UserTypeForm
    if request.method == "POST":
        form = UserTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succesfully Added")
            return redirect(user_type_add)
        else:
            messages.error(request, "Something Wrong")
            return redirect(user_type_add)
    return render(request, 'adminpanel/admin-user-type-add.html', {'form':form})

def user_type_delete(request,pk):
    UserType.objects.filter(id=int(pk)).delete()
    messages.success(request, "Deleted Succesfully")
    return redirect(user_type)



#Property <---->
def admin_add_property(request):
    property_for = PropertyFor.objects.all()
    property_type = PropertyType.objects.all()
    property_data = Property()
    context = {
        "property_for":property_for,
        "property_type":property_type,
        "furnishing_status":property_data.FurnishingStatus,
        "available_for":property_data.AvailableFor,
        "property_status":property_data.PropertyStatus,
    }
    if request.method == "POST":
        title              = request.POST.get('title')
        slug               = request.POST.get('slug')
        price              = request.POST.get('price')
        body               = request.POST.get('body')
        description        = request.POST.get('description')
        locality           = request.POST.get('locality')
        bedroom            = request.POST.get('bedroom')
        bathroom           = request.POST.get('bathroom')
        balcony            = request.POST.get('balcony')
        locality           = request.POST.get('locality')
        carpet_area        = request.POST.get('carpet_area')
        builtup_area       = request.POST.get('builtup_area')
        superbuiltup_area  = request.POST.get('superbuiltup_area')
        floors             = request.POST.get('floors')
        property_age       = request.POST.get('property_age')
        property_status    = request.POST.get('property_status')
        furnishing_status  = request.POST.get('furnishing_status')
        available_for      = request.POST.get('available_for')
        images            = request.POST.getlist('image')
        parking            = request.POST.get('parking')

    return render(request, 'adminpanel/admin-add-property.html', context)

def admin_location(request):
    return render(request, 'adminpanel/admin-location.html')

def admin_country_list(request):
    data = Country.objects.all()
    return render(request, 'adminpanel/admin-country-list.html',{'data':data})

def country_add(request):
    form = CountryForm
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Succesfully Added' )
            return redirect(country_add) 
        else:
            messages.error(request,'Name is already in use.' )
            return redirect(country_add)
    return render(request, 'adminpanel/admin-country-add.html',{'form':form})

def country_delete(request, pk):
    Country.objects.filter(id=int(pk)).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect(admin_country_list)

def admin_state_list(request):
    data = State.objects.all()
    return render(request, 'adminpanel/admin-state-list.html',{'data':data})

def state_add(request):
    form = StateForm
    if request.method == "POST":
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succesfully Added")
            return redirect(state_add)
        else:
            messages.error(request, 'Name is already in use.')
            return redirect(state_add)
    return render(request, 'adminpanel/admin-state-add.html', {'form':form})

def state_delete(request, pk):
    State.objects.filter(id=int(pk)).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect(admin_state_list)

def admin_city_list(request):
    data = City.objects.all()
    return render(request, 'adminpanel/admin-city-list.html', {'data':data})

def city_add(request):
    form = CityForm
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added")
            return redirect(city_add)
        else:
            messages.error(request, "Name is already in use.")
            return redirect(city_add)
    return render(request, 'adminpanel/admin-city-add.html',{'form':form})

def city_delete(request, pk):
    City.objects.filter(id=int(pk)).delete()
    messages.success(request, "Deleted Successfully")
    return redirect(admin_city_list)