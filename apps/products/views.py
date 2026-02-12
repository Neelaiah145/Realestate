from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property,PropertyImage,PropertyFeature,PropertyLocation
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required




@login_required
def property_list(request):
    qs = Property.objects.prefetch_related("images").all()

    if not request.user: #.is_superuser:
        qs = qs.filter(agent=request.user)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    status = request.GET.get("status")

    if min_price:
        qs = qs.filter(price__gte=min_price)

    if max_price:
        qs = qs.filter(price__lte=max_price)

    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)

    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)

    if status:
        qs = qs.filter(property_status=status)

 
    for p in qs:
        p.primary_image = p.images.filter(is_primary=True).first()
    paginator = Paginator(qs, 6)   # 6 properties per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "property/property_list.html", {
        "properties": qs,
         "properties": page_obj,
         "page_title":"All Propertys"
        
    })
 

@permission_required('products.add_property', raise_exception=True)
@login_required
def property_create(request):
    if request.method == "POST":
        prop = Property.objects.create(
            property_type=request.POST.get("property_type"),
            property_status=request.POST.get("property_status"),
            price=request.POST.get("price"),
            property_price=request.POST.get("property_price"),
            max_rooms=request.POST.get("max_rooms"),
            beds=request.POST.get("beds"),
            baths=request.POST.get("baths"),
            area=request.POST.get("area"),
            premiere=request.POST.get("premiere"),
            description=request.POST.get("description"),
            address=request.POST.get("address"),
            zip_code=request.POST.get("zip_code"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            country=request.POST.get("country"),
            property_size=request.POST.get("property_size"),
            garage=request.POST.get("garage"),
            year_built=request.POST.get("year_built") or None,
            is_featured=True if request.POST.get("is_featured") else False,
            agent=request.user
        )

     
        PropertyLocation.objects.create(
            property=prop,
            latitude=request.POST.get("latitude") or None,
            longitude=request.POST.get("longitude") or None,
            area_name=request.POST.get("area_name")
        )

  
        features = request.POST.getlist("features[]")
        for f in features:
            PropertyFeature.objects.create(property=prop, feature_name=f)

        images = request.FILES.getlist("images")
        for i, img in enumerate(images):
            PropertyImage.objects.create(
                property=prop,
                image=img,
                is_primary=True if i == 0 else False
            )

        return redirect("property_list")

    return render(request, "property/property_form.html",{"page_title":"Create Property"})



# update the product

@permission_required('products.change_property', raise_exception=True)
@login_required
def property_update(request, pk):
    prop = get_object_or_404(Property, pk=pk)


    
    if request.method == "POST":

        fields = [
            "property_type", "property_status", "price", "property_price",
            "max_rooms", "beds", "baths", "area", "premiere",
            "description", "address", "zip_code", "city",
            "state", "country", "property_size",
            "garage", "garage_size", "year_built"
        ]

        for field in fields:
            setattr(prop, field, request.POST.get(field))

        prop.is_featured = True if request.POST.get("is_featured") else False
        prop.save()

        location, _ = PropertyLocation.objects.get_or_create(property=prop)
        location.latitude = request.POST.get("latitude") or None
        location.longitude = request.POST.get("longitude") or None
        location.area_name = request.POST.get("area_name")
        location.save()

        prop.features.all().delete()
        features = request.POST.getlist("features[]")
        for f in features:
            PropertyFeature.objects.create(property=prop, feature_name=f)

    
        images = request.FILES.getlist("images")
        for img in images:
            PropertyImage.objects.create(property=prop, image=img)

        return redirect("property_list")

    return render(request, "property/property_form.html", {
        "property": prop,
        "location": getattr(prop, "location_details", None),
        "features": prop.features.all(),
        "images": prop.images.all()
    })




# delete the product
@permission_required('products.delete_property', raise_exception=True)
@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)


    if request.method == "POST":
        prop.delete()
        return redirect("property_list")

    return render(request, "property/property_delete.html", {
        "property": prop,
        "page_title":"Delete Property",
    })



# about the product
def about_property(request, pk):
    property_obj = get_object_or_404(
        Property.objects
        .select_related("agent", "location_details")
        .prefetch_related("images", "features"),
        pk=pk
    )

    return render(request, "property/about_property.html", {
        "property": property_obj,
        "page_title":"Property Details"
    })




# agent