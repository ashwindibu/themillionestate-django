from itertools import count
from math import floor
from multiprocessing import context
from turtle import Turtle, title
from urllib.request import HTTPPasswordMgrWithDefaultRealm
from venv import create
from django.contrib import messages
from django.shortcuts import redirect, render
import os
from .forms import PropertyTypeForm, PropertyForForm, CountryForm, StateForm, CityForm, FeaturesForm
from property.models import PropertyType, PropertyFor, Property,Country, State, City, Image,Features
from base.models import  Account
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import authenticate

# Create your views here.

def admin_login(request):
    if request.session.has_key('admin'):
        return redirect(home)
    if request.method == "POST":
        admin_email = request.POST.get('email')
        admin_password = request.POST.get('password')
        print(admin_email, admin_password)
        admin = authenticate(email=admin_email, password=admin_password)
        if admin is not None:
            if admin.is_superadmin:
                request.session['admin'] = admin_email
                return redirect(home)
            else:
                messages.error(request, "You are not Authorized")
                return render(request, 'adminpanel/admin-login.html')
        else:
            messages.error(request,"Invalid Credentials")
            return render(request, 'adminpanel/admin-login.html')
    return render(request, 'adminpanel/admin-login.html')

def home(request):
    if request.session.has_key('admin'):
        total_property = Property.objects.all().count()
        context = {
            "total_property":total_property
        }
        return render(request, 'adminpanel/adminhome.html', context)
    else:
        return redirect(admin_login)
def admin_logout(request):
    if request.session.has_key('admin'):
        request.session.flush()
    return redirect(admin_login)
    
#PropertyType <---->
def admin_property_type(request):
    if request.session.has_key('admin'):
        property_types = PropertyType.objects.all()
        count = property_types.count()
        context = {
            "data":property_types,
            "count":count
        }
        return render(request, 'adminpanel/admin-property-type.html', context)
    else:
        return redirect(admin_login)

def admin_property_type_add(request):
    if request.session.has_key('admin'):
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
    else:
        return redirect(admin_login)

def admin_property_type_delete(request, pk):
    PropertyType.objects.filter(id=int(pk)).delete()
    return redirect(admin_property_type)



#PropertyFor <---->
def admin_property_for(request):
    if request.session.has_key('admin'):
        property_for = PropertyFor.objects.all()
        return render(request, 'adminpanel/admin-property-for.html',{"data":property_for})
    else:
        return redirect(admin_login)

def property_for_add(request):
    if request.session.has_key('admin'):
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
    else:
        return redirect(admin_login)

def property_for_delete(request,pk):
    PropertyFor.objects.filter(id=int(pk)).delete()
    return redirect(admin_property_for)



# #UserType <---->
# def user_type(request):
#     if request.session.has_key('admin'):
#         user_type = UserType.objects.all()
#         return render(request, "adminpanel/admin-user-type.html", {'data':user_type })
#     else:
#         return redirect(admin_login)

# def user_type_add(request):
#     if request.session.has_key('admin'):
#         form = UserTypeForm
#         if request.method == "POST":
#             form = UserTypeForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Succesfully Added")
#                 return redirect(user_type_add)
#             else:
#                 messages.error(request, "Something Wrong")
#                 return redirect(user_type_add)
#         return render(request, 'adminpanel/admin-user-type-add.html', {'form':form})
#     else:
#         return redirect(admin_login)

# def user_type_delete(request,pk):
#     UserType.objects.filter(id=int(pk)).delete()
#     messages.success(request, "Deleted Succesfully")
#     return redirect(user_type)





def admin_property_list(request):
    if request.session.has_key('admin'):
        property_details    = Property.objects.all().order_by('id')
        paginator = Paginator(property_details, 6)
        page = request.GET.get('page')
        paged_property =  paginator.get_page(page)
        return render(request, 'adminpanel/admin-property-list.html',{'datas':paged_property,})
    else:
        return redirect(admin_login)

#Property ADD <---->
def admin_add_property(request):
    if request.session.has_key('admin'):
        property_for    = PropertyFor.objects.all()
        property_type   = PropertyType.objects.all()
        property_data   = Property()
        city            = City.objects.all()
        features_form           = FeaturesForm(request.POST or None)
        context = {
            "property_for":property_for,
            "property_type":property_type,
            "furnishing_status":property_data.FurnishingStatus,
            "available_for":property_data.AvailableFor,
            "property_status":property_data.PropertyStatus,
            "city":city,
            "features_form":features_form,
        }
        if request.method == "POST":
            titledemo          = request.POST.get('title')
            slug               = request.POST.get('slug')
            price              = request.POST.get('property_price')
            body               = request.POST.get('body')
            description        = request.POST.get('description')
            locality           = request.POST.get('locality')
            bedroom            = request.POST.get('bedroom')
            bathroom           = request.POST.get('bathroom')
            balcony            = request.POST.get('balcony')
            carpet_area        = request.POST.get('carpet_area')
            builtup_area       = request.POST.get('builtup_area')
            superbuiltup_area  = request.POST.get('superbuiltup_area')
            floors             = request.POST.get('floor')
            property_age       = request.POST.get('property_age')
            property_status    = request.POST.get('property_status')
            furnishing_status  = request.POST.get('furnishing_status')
            available_for      = request.POST.get('available_for')
            featured_image     = request.FILES.get('featured_image')
            parking            = request.POST.get('parking')
            publish             = request.POST.get('publish')
            property_for_data  = request.POST.get('property-for')
            property_type_data = request.POST.get('property-type')
            city               = request.POST.get('city')
            account            = Account.objects.get(is_superadmin=1)
            if builtup_area=='':
                builtup_area=None
            if superbuiltup_area=='':
                superbuiltup_area=None
            if property_age=='':
                property_age=None
            if parking=='':
                parking=None
            if balcony=='':
                balcony=None
            
            # Publishing On or Off
            print(publish)
            print(floors)
            print("Hello ", property_type_data)
            if publish:
                publish_on = True
            else:
                publish_on = False

            # Auto Generated Title
            propertytype       = PropertyType.objects.get(id=property_type_data)
            bhk     = str(bedroom) + " BHK "
            title   = bhk + propertytype.property_type_name+" in "+ str(locality)
            print(title)

            # Indian Currency Format Words
            def format_indian(t):
                dic = {
                    4:'Thousand',
                    5:'Lakh',
                    6:'Lakh',
                    7:'Crore',
                    8:'Crore',
                    9:'Billion'
                }
                y = 10
                len_of_number = len(str(t))
                save = t
                z=y
                while(t!=0):
                    t=int(t/y)
                    z*=10

                zeros = len(str(z)) - 3
                if zeros>3:
                    if zeros%2!=0:
                        string = str(save/(z/100))[0:4]+" "+dic[zeros]
                    else:   
                        string = str(save/(z/1000))[0:4]+" "+dic[zeros]
                    return string
                return str(save)
            if price:
                indian_currency = format_indian(int(price))
                print(indian_currency)

            
            property_details = Property.objects.create(
                property_for_id_id = property_for_data,
                property_type_id_id = property_type_data,
                city_id_id = city,
                locality = locality,
                bedroom = bedroom,
                bathroom = bathroom,
                balcony = balcony,
                carpet_area = carpet_area,
                builtup_area = builtup_area,
                superbuiltup_area = superbuiltup_area,
                floors = floors,
                property_age = property_age,
                parking = parking,
                title = title,
                description = description, 
                price = price,
                indian_currency = indian_currency,
                furnishing_status = furnishing_status,
                available_for = available_for,
                property_status = property_status,
                featured_image = featured_image,
                published = publish_on,
                user_id = account,
                )
            print(features_form)
            if features_form.is_valid():
                print(features_form.cleaned_data)
                features = Features()
                features.property_id_id = property_details.id
                features.swimming_pool = features_form.cleaned_data['swimming_pool']
                features.visitor_parking = features_form.cleaned_data['visitor_parking']
                features.power_backup = features_form.cleaned_data['power_backup']
                features.security_firealarm = features_form.cleaned_data['security_firealarm']
                features.lift = features_form.cleaned_data['lift']
                features.fitness_centre = features_form.cleaned_data['fitness_centre']
                features.childrens_park = features_form.cleaned_data['childrens_park']
                features.club_house = features_form.cleaned_data['club_house']
                features.multipurpose_room = features_form.cleaned_data['multipurpose_room']
                features.sports_facility = features_form.cleaned_data['sports_facility']
                features.rain_water_harvesting = features_form.cleaned_data['rain_water_harvesting']
                features.intercom = features_form.cleaned_data['intercom']
                features.maintenance_staff = features_form.cleaned_data['maintenance_staff']
                features.water_purifier = features_form.cleaned_data['water_purifier']
                features.vaastu_compliant = features_form.cleaned_data['vaastu_compliant']
                features.natural_light = features_form.cleaned_data['natural_light']
                features.wifi_connectivity = features_form.cleaned_data['wifi_connectivity']
                features.atm = features_form.cleaned_data['atm']
                features.waste_disposal = features_form.cleaned_data['waste_disposal']
                features.piped_gas = features_form.cleaned_data['piped_gas']
                features.save()
                print("Entered Feature Form")

            images             = request.FILES.getlist('image')
            print(property_details )
            if images:
                for image in images:
                    img = Image()
                    img.property = property_details
                    img.image = image
                    img.save()

            print(property_details.id)
            messages.success(request,'Property Added Succesfully')
            return redirect(admin_property_list)
        
        return render(request, 'adminpanel/admin-add-property.html', context)
    else:
        return redirect(admin_login)



#Property Edit
def admin_edit_property(request, pk):
    if request.session.has_key('admin'):
        pk              = int(pk)
        property        = Property.objects.get(id=pk)
        property_image  = Image.objects.all().filter(property=pk)
        property_for    = PropertyFor.objects.all()
        property_type   = PropertyType.objects.all()
        property_data   = Property()
        city            = City.objects.all()
        featured_image_check = False
        if property.featured_image:
            featured_image_check = True


        features_data_f = Features.objects.filter(property_id_id=pk)
        if features_data_f:
            features_data = Features.objects.get(property_id_id=pk)
            features_form = FeaturesForm(instance=features_data)
        else:
            features_form = FeaturesForm()
            
        context = {
            "property":property,
            "property_for":property_for,
            "property_type":property_type,
            "furnishing_status":property_data.FurnishingStatus,
            "available_for":property_data.AvailableFor,
            "property_status":property_data.PropertyStatus,
            "city":city,
            "property_image":property_image,
            "featrued_image_check":featured_image_check,
            "features_form":features_form
        }

        if request.method == "POST" and 'btnform1':
            titledemo          = request.POST.get('title')
            slug               = request.POST.get('slug')
            price              = request.POST.get('property_price')
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
            floors             = request.POST.get('floor')
            property_age       = request.POST.get('property_age')
            property_status    = request.POST.get('property_status')
            furnishing_status  = request.POST.get('furnishing_status')
            available_for      = request.POST.get('available_for')
            featured_image     = request.FILES.get('featured_image')
            parking            = request.POST.get('parking')
            publish            = request.POST.get('publish')
            property_for_data  = request.POST.get('property-for')
            property_type_data = request.POST.get('property-type')
            city               = request.POST.get('city')
            account            = request.user
            print(account)
            if featured_image: 
                if property.featured_image:
                    if os.path.exists(property.featured_image.path):
                        os.remove(property.featured_image.path)
            else:
                if property.featured_image:
                    if os.path.exists(property.featured_image.path):
                        featured_image = property.featured_image
            if builtup_area=='':
                builtup_area=None
            if superbuiltup_area=='':
                superbuiltup_area=None
            if property_age=='':
                property_age=None
            if parking=='':
                parking=None
            if balcony=='':
                balcony=None
            if floors=='':
                floors=None
    

            # Publishing On or Off
            print(bedroom)
            print(publish)
            print("Hello ", property_type_data)
            if publish:
                publish_on = True
            else:
                publish_on = False

            # Auto Generated Title
            propertytype       = PropertyType.objects.get(id=property_type_data)
            bhk     = str(bedroom) + " BHK "
            title   = bhk + propertytype.property_type_name+" in "+ str(locality)
            print(title)

            # Indian Currency Format Words
            def format_indian(t):
                dic = {
                    4:'Thousand',
                    5:'Lakh',
                    6:'Lakh',
                    7:'Crore',
                    8:'Crore',
                    9:'Billion'
                }
                y = 10
                len_of_number = len(str(t))
                save = t
                z=y
                while(t!=0):
                    t=int(t/y)
                    z*=10

                zeros = len(str(z)) - 3
                if zeros>3:
                    if zeros%2!=0:
                        string = str(save/(z/100))[0:4]+" "+dic[zeros]
                    else:   
                        string = str(save/(z/1000))[0:4]+" "+dic[zeros]
                    return string
                return str(save)
            if price:
                indian_currency = format_indian(int(price))
                print(indian_currency)


            property.property_for_id_id = property_for_data
            property.property_type_id_id = property_type_data
            property.city_id_id = city
            property.locality = locality
            property.bedroom = bedroom
            property.bathroom = bathroom
            property.balcony = balcony
            property.carpet_area = carpet_area
            property.builtup_area = builtup_area
            property.superbuiltup_area = superbuiltup_area
            property.floors = floors
            property.property_age = property_age
            property.parking = parking
            property.title = title
            property.description = description
            property.price = price
            property.indian_currency = indian_currency
            property.furnishing_status = furnishing_status
            property.available_for = available_for
            property.property_status = property_status
            property.featured_image = featured_image
            property.published = publish_on
            property.user_id = account
            property.save()

            # Property.objects.filter(id=pk).update(
            #     property_for_id_id = property_for_data,
            #     property_type_id_id = property_type_data,
            #     city_id_id = city,
            #     locality = locality,
            #     bedroom = bedroom,
            #     bathroom = bathroom,
            #     balcony = balcony,
            #     carpet_area = carpet_area,
            #     builtup_area = builtup_area,
            #     superbuiltup_area = superbuiltup_area,
            #     floors = floors,
            #     property_age = property_age,
            #     parking = parking,
            #     title = title,
            #     description = description, 
            #     price = price,
            #     indian_currency = indian_currency,
            #     furnishing_status = furnishing_status,
            #     available_for = available_for,
            #     property_status = property_status,
            #     featured_image = featured_image,
            #     published = publish_on,
            #     user_id = account,
            #     )
            features_form = FeaturesForm(request.POST)
            if features_form.is_valid():
                print(features_form.cleaned_data)
                features_data_f = Features.objects.filter(property_id_id=pk)
                if features_data_f:
                    features = Features.objects.get(property_id_id=pk)
                    features.property_id_id = pk

                else:
                    features = Features()
                features.property_id_id = pk
                features.swimming_pool = features_form.cleaned_data['swimming_pool']
                features.visitor_parking = features_form.cleaned_data['visitor_parking']
                features.power_backup = features_form.cleaned_data['power_backup']
                features.security_firealarm = features_form.cleaned_data['security_firealarm']
                features.lift = features_form.cleaned_data['lift']
                features.fitness_centre = features_form.cleaned_data['fitness_centre']
                features.childrens_park = features_form.cleaned_data['childrens_park']
                features.club_house = features_form.cleaned_data['club_house']
                features.multipurpose_room = features_form.cleaned_data['multipurpose_room']
                features.sports_facility = features_form.cleaned_data['sports_facility']
                features.rain_water_harvesting = features_form.cleaned_data['rain_water_harvesting']
                features.intercom = features_form.cleaned_data['intercom']
                features.maintenance_staff = features_form.cleaned_data['maintenance_staff']
                features.water_purifier = features_form.cleaned_data['water_purifier']
                features.vaastu_compliant = features_form.cleaned_data['vaastu_compliant']
                features.natural_light = features_form.cleaned_data['natural_light']
                features.wifi_connectivity = features_form.cleaned_data['wifi_connectivity']
                features.atm = features_form.cleaned_data['atm']
                features.waste_disposal = features_form.cleaned_data['waste_disposal']
                features.piped_gas = features_form.cleaned_data['piped_gas']
                features.save()
                print("Entered Feature Form")
            images             = request.FILES.getlist('image')
            if images:
                for image in images:
                    img = Image()
                    img.property = property
                    img.image = image
                    img.save()
            messages.success(request, 'Property Updated Successfully')            
            return redirect(admin_property_list)

        if request.method == "POST" and 'btnform2':
            image_id = request.POST.getlist('id[]')
            print("Entered Ajax", image_id)
            for id in image_id:
                print("Entered Loop", id)
                image_data = Image.objects.get(id=id)
                image_data.delete()
        return render(request, 'adminpanel/admin-edit-property.html', context)
    else:
        return redirect(admin_login)

def admin_property_delete(request, pk):
    Property.objects.filter(id=pk).delete()
    messages.success(request,'Property Deleted Succesfully')
    return redirect(admin_property_list)


def admin_location(request):
    if request.session.has_key('admin'):
        return render(request, 'adminpanel/admin-location.html')
    else:
        return redirect(admin_login)

def admin_country_list(request):
    if request.session.has_key('admin'):
        data = Country.objects.all()
        return render(request, 'adminpanel/admin-country-list.html',{'data':data})
    else:
        return redirect(admin_login)

def country_add(request):
    if request.session.has_key('admin'):
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
    else:
        return redirect(admin_login)

def country_delete(request, pk):
    Country.objects.filter(id=int(pk)).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect(admin_country_list)

def admin_state_list(request):
    if request.session.has_key('admin'):
        data = State.objects.all()
        return render(request, 'adminpanel/admin-state-list.html',{'data':data})
    else:
        return redirect(admin_login)

def state_add(request):
    if request.session.has_key('admin'):
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
    else:
        return redirect(admin_login)

def state_delete(request, pk):
    State.objects.filter(id=int(pk)).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect(admin_state_list)

def admin_city_list(request):
    if request.session.has_key('admin'):
        data = City.objects.all()
        return render(request, 'adminpanel/admin-city-list.html', {'data':data})
    else:
        return redirect(admin_login)

def city_add(request):
    if request.session.has_key('admin'):
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
    else:
        return redirect(admin_login)

def city_delete(request, pk):
    City.objects.filter(id=int(pk)).delete()
    messages.success(request, "Deleted Successfully")
    return redirect(admin_city_list)