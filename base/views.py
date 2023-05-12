import re, os
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from property.models import Image, Property, PropertyFor, PropertyType, City, State, Features
from django.db.models import Q
from django.contrib import messages, auth
from .models import Account
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm ,UserProfileForm, FeaturesForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    latest_propertys = Property.objects.all().filter(published=True).order_by("-created_at")[:9]
    property_types   = PropertyType.objects.all()
    property_for     = PropertyFor.objects.all()

    context = {
        "latest_propertys":latest_propertys,
        "property_types":property_types,
        "property_for":property_for,
    }
    return render(request, 'index.html',context)

def suggestionapi(request):
    if "term" in request.GET:
        search = request.GET.get('term')
        qs = Property.objects.filter(Q(locality__icontains=search))[0:10]
        titles = list()
        print("hello ", qs)
        for property in qs:
            titles.append(property.locality)
        if len(qs)<10:
            length = 10 - len(qs)
            qs2 = Property.objects.filter(Q(locality__icontains=search))[0:length]
            for property in qs2:
                titles.append(property.locality)
        return JsonResponse(titles, safe=False)
        

def contact(request):
    return render(request, 'contact.html')

def propertys(request, category_slug=None):
    categories          = None
    property            = None
    search              = request.GET.get('search')
    property_type       = request.GET.get('property-type')
    property_status     = request.GET.get('property-status')
    property_beds       = request.GET.get('property-beds')
    property_baths      = request.GET.get('property-baths')

    def is_valid_queryparam(param):
        return param != '' and param is not None

    property = Property.objects.all().filter(published=True).order_by('-created_at')
    ordering        = request.GET.get('ordering', "")
    if ordering:
        property        = property.order_by(ordering)
    paginator       = Paginator(property, 6)
    page            = request.GET.get('page')
    propertys       = paginator.get_page(page)

    property_types  = PropertyType.objects.all()
    proprety_status2 = PropertyFor.objects.all()


    if is_valid_queryparam(search):
        property = property.filter(Q(locality__icontains=search))
        ordering        = request.GET.get('ordering', "") 
        if ordering:
            property        = property.filter(Q(locality__icontains=search)).order_by(ordering)
        paginator       = Paginator(property, 6)
        page            = request.GET.get('page')
        propertys       = paginator.get_page(page)

    if is_valid_queryparam(property_type):
        int(property_type)
        property = property.filter(property_type_id=property_type)
        ordering        = request.GET.get('ordering', "") 
        if ordering:
            property        = property.filter(Q(property_type_id=property_type)).order_by(ordering)
        paginator       = Paginator(property, 6)
        page            = request.GET.get('page')
        propertys       = paginator.get_page(page)
    
    if is_valid_queryparam(property_status):
        int(property_status)
        property = property.filter(property_for_id=property_status)
        ordering        = request.GET.get('ordering', "") 
        if ordering:
            property        = property.filter(property_for_id=property_status).order_by(ordering)
        paginator       = Paginator(property, 6)
        page            = request.GET.get('page')
        propertys       = paginator.get_page(page)

    if is_valid_queryparam(property_beds):
        int(property_beds)
        property = property.filter(bedroom=property_beds)
        ordering        = request.GET.get('ordering', "") 
        if ordering:
            property        = property.filter(edroom=property_beds).order_by(ordering)
        paginator       = Paginator(property, 6)
        page            = request.GET.get('page')
        propertys       = paginator.get_page(page)

    if is_valid_queryparam(property_baths):
        int(property_baths)
        property = property.filter(bathroom=property_baths)
        ordering        = request.GET.get('ordering', "") 
        if ordering:
            property        = property.filter(bathroom=property_baths).order_by(ordering)
        paginator       = Paginator(property, 6)
        page            = request.GET.get('page')
        propertys       = paginator.get_page(page)

    if is_valid_queryparam(category_slug):
        categories  = get_object_or_404(PropertyType, slug = category_slug )
        property = Property.objects.all().filter(property_type_id=categories, published=True).order_by('-created_at')
        ordering        = request.GET.get('ordering', "")
        if ordering:
            property        = Property.objects.all().filter(property_type_id=categories, published=True).order_by(ordering)
        paginator       = Paginator(property, 6)
        page            = request.GET.get('page')
        propertys       = paginator.get_page(page)
    # propertys       = Property.objects.all()[:6]

    # else:
    #     property = Property.objects.all().filter(published=True).order_by('-created_at')
    #     ordering        = request.GET.get('ordering', "")
    #     if ordering:
    #         property        = Property.objects.all().filter(published=True).order_by(ordering)
    #     paginator       = Paginator(property, 6)
    #     page            = request.GET.get('page')
    #     propertys       = paginator.get_page(page)


    context = {
        'propertys':propertys,
        'property_types':property_types,
        'property_status':proprety_status2,
        'property_for':proprety_status2,
        'property_type_category':categories,
    
      
    }
    return render(request, 'propertys.html', context)

def property_single(request, pk):
    pk          = int(pk)
    similar_property = Property.objects.all().filter(published=True).order_by('-created_at')[:6]
    property    = Property.objects.get(id=pk)
    try:
        property_features = Features.objects.get(property_id_id = pk)
    except:
        property_features = None
    image             = Image.objects.filter(property_id=pk)
    
    context = {
        'similar_property':similar_property,
        'property':property,
        'image':image,
        'features':property_features,
    }
    return render(request, 'property-single.html', context)

# def user_signup(request):
#     def validate_email_address(email_address):
#         if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address):
#             print(f"The email address {email_address} is not valid")
#             return False
#         else:
#             print("valid email")
#             return True
            
#     if request.method == "POST":
#         full_name           = request.POST['full_name']
#         register_email      = request.POST['register_email']
#         register_password   = make_password(request.POST['register_password'])
#         if validate_email_address(register_email):
#             if Account.objects.filter(email=register_email):
#                 return JsonResponse(
#                     {'success': False, "message":f"The email address: {register_email} is already registered"},
#                     safe=False
#                 )
#             else:
#                 Account.objects.create(full_name=full_name, email=register_email, password=register_password)
#                 return JsonResponse(
#                     {'success': True},
#                     safe=False
#                 )
#         else:
#             return JsonResponse(
#                 {'success': False, "message":f"The email address: {register_email} is not valid"},
#                 safe=False
#             )
#     else:
#         messages.info(request,"Successfuly")
#         return redirect(home)

# def user_login(request):
#     if request.method =="POST":
#         email       = request.POST['user_email']
#         password    = request.POST['user_password']
#         print(email," ", password)
#         user        = auth.authenticate(email=email, password=password)
#         print(user)
#         if user is not None:
#             print("hello")
#             print(user)
#             print(user.password)
#             if check_password()
#             login(request, user)
#             return JsonResponse(
#                 {'success': True, "message":f"Successfully Login"},
#                 safe=False
#             )
#         else:
#             return JsonResponse(
#                 {'success': False, "message":f"Credential are not valid"},
#                 safe=False
#             )
# def user_login(request):
#     return render(request, 'account/login.html')

def user_login(request):
    if request.method == 'POST':
        
        email       = request.POST.get('user_email')
        password    = request.POST.get('user_password')
        user = authenticate(request, email=email, password=password)
        print('hello login \n hey its me login'+email, password)


        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Email or Password is incorrect')
            return redirect('accounts/login')

    

def user_logout(request):
    logout(request)
    return redirect(home)

def user_register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(home)

    context = {
        "form":form
    }
    return render(request, 'account/user-register.html', context)

def user_profile(request):
    user = request.user
    form = UserProfileForm(instance=user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        print('profile entered Method')

        if form.is_valid():
            print('profile form added sucessfully')
            form.save()
    context = {'form':form}
    return render(request, 'user-profile.html', context)

def my_property(request):
    user = request.user
    
    user_id = int(user.id)
    property = Property.objects.all().filter(user_id_id=user_id)
    print(property)
    paginator       = Paginator(property, 6)
    page            = request.GET.get('page')
    property_details      = paginator.get_page(page)
    context = {
        'datas':property_details
    }
    return render(request, 'my-property.html',context)

def favourite_property(request):
    return render(request, 'favourite-property.html')

@login_required
def add_property(request):
    property_for        = PropertyFor.objects.all()
    property_type       = PropertyType.objects.all()
    property_data       = Property()
    city                = City.objects.all()
    features_form       = FeaturesForm(request.POST or None)
    context = {
        "property_for":property_for,
        "property_type":property_type,
        "furnishing_status":property_data.FurnishingStatus,
        "available_for":property_data.AvailableFor,
        "property_status":property_data.PropertyStatus,
        "city":city,
        "features_form":features_form
    }

    if request.method == "POST":
        price           = request.POST.get('property_price')
        description     = request.POST.get('description')
        locality        = request.POST.get('locality')
        bedroom         = request.POST.get('bedroom')
        bathroom        = request.POST.get('bathroom')
        balcony         = request.POST.get('balcony')
        carpet_area     = request.POST.get('carpet_area')
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
        accounts           = Account.objects.get(email=request.user)
        accountid          = accounts.id
        if builtup_area=='':
            builtup_area=None
        if superbuiltup_area=='':
            superbuiltup_area=None
        if property_age=='':
            property_age==None
        if parking=='':
            parking=None
        if balcony=='':
            balcony=None
        print(publish)
        print(floors)
        print(accountid)
        print("Hello ", property_type_data)
        if publish:
            publish_on = True
        else:
            publish_on = False  
        
        # Auto Generated Title
        propertytype       = PropertyType.objects.get(id=property_type_data)
        bhk                = str(bedroom) + " BHK "
        title              = bhk + propertytype.property_type_name+" in "+ str(locality)
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
            property_for_id_id      = property_for_data,
            property_type_id_id     = property_type_data,
            city_id_id              = city,
            locality                = locality,
            bedroom                 = bedroom,
            bathroom                = bathroom,
            balcony                 = balcony,
            carpet_area             = carpet_area,
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
            user_id_id = accountid,
        )
        print(features_form)
        if features_form.is_valid():
            print(features_form.cleaned_data)
            features = Features()
            features.property_id_id = property_details.id
            features.swimming_pool  = features_form.cleaned_data['swimming_pool']
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
        print(property_details)
        if images:
            for image in images:
                img = Image()
                img.property = property_details
                img.image = image
                img.save()

        print(property_details.id)
        messages.success(request,'Property Added Succesfully')
        return redirect(my_property)

    return render(request, 'add-property.html', context)

@login_required
def my_property_edit(request, pk):
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
        return redirect(my_property)

    if request.method == "POST" and 'btnform2':
        image_id = request.POST.getlist('id[]')
        print("Entered Ajax", image_id)
        for id in image_id:
            print("Entered Loop", id)
            image_data = Image.objects.get(id=id)
            image_data.delete()

    return render(request, 'my_property_edit.html', context)

def my_property_delete(request, pk):
    Property.objects.filter(id=pk).delete()
    messages.success(request, 'Property Deleted Successfully')
    return redirect(my_property)

