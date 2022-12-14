import re
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from property.models import Image, Property, PropertyFor, PropertyType, City, State, Features
from django.db.models import Q
from django.contrib import messages, auth
from .models import Account
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm ,UserProfileForm
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
    pk = int(pk)
    property = Property.objects.get(id=pk)
    
    image    = Image.objects.filter(property_id=pk)
    
    context = {
        'property':property,
        'image':image
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
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'user-profile.html', context)

def my_property(request):
    return render(request, 'my-property.html')

def favourite_property(request):
    return render(request, 'favourite-property.html')

@login_required
def add_property(request):
  
    return render(request, 'add-property.html')
