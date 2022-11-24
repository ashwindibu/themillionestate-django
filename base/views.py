from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from property.models import Image, Property, PropertyFor, PropertyType
from django.db.models import Q

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

def login(request):
    return render(request,'login.html')