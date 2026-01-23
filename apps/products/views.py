from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, PropertyImage, PropertyFeature
from django.core.paginator import Paginator


@login_required
def add_property(request):
    """View to add a new property"""
    if request.method == 'POST':
        try:
            # Get price value, use property_price if price is not provided
            price_value = request.POST.get('price')
            if not price_value:
                price_value = request.POST.get('property_price')
            
            # Create property instance
            property_instance = Property.objects.create(
                property_type=request.POST.get('property_type'),
                property_status=request.POST.get('property_status'),
                property_price=request.POST.get('property_price'),
                max_rooms=request.POST.get('max_rooms'),
                beds=request.POST.get('beds'),
                baths=request.POST.get('baths'),
                area=request.POST.get('area'),
                price=price_value,
                premiere=request.POST.get('premiere'),
                description=request.POST.get('description', ''),
                address=request.POST.get('address'),
                zip_code=request.POST.get('zip_code'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country=request.POST.get('country'),
                agent=request.user
            )
            
            # Handle multiple image uploads
            images = request.FILES.getlist('property_images')
            if images:
                for index, image in enumerate(images):
                    PropertyImage.objects.create(
                        property=property_instance,
                        image=image,
                        is_primary=(index == 0)  # First image is primary
                    )
            
            messages.success(request, f'Property {property_instance.property_id} added successfully!')
            return redirect('property_list')
            
        except Exception as e:
            messages.error(request, f'Error adding property: {str(e)}')
    
    context = {
        'page_title': 'Add Property'
    }
    return render(request, 'products/add_property.html', context)


@login_required
def property_list(request):
    """View to display all properties"""
    # Get all properties for the logged-in user
    properties = Property.objects.all().prefetch_related('images', 'agent')
    
    # Sorting
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price_low':
        properties = properties.order_by('property_price')
    elif sort_by == 'price_high':
        properties = properties.order_by('-property_price')
    elif sort_by == 'newest':
        properties = properties.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(properties, 9)  # 9 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Property List',
        'properties': page_obj,
        'total_properties': properties.count(),
        'sort_by': sort_by
    }
    return render(request, 'products/property_list.html', context)


@login_required
def property_details(request, property_id=None):
    """View to display property details"""
    if property_id:
        property_instance = get_object_or_404(Property, id=property_id)
    else:
        # Get the first property or show message
        property_instance = Property.objects.first()
        if not property_instance:
            messages.info(request, 'No properties available. Please add a property first.')
            return redirect('add_property')
    
    # Get all images for this property
    images = property_instance.images.all()
    
    # Get features
    features = property_instance.features.all()
    
    context = {
        'page_title': f'Property Details - {property_instance.property_id}',
        'property': property_instance,
        'images': images,
        'features': features
    }
    return render(request, 'products/property_details.html', context)


@login_required
def edit_property(request, property_id):
    """View to edit an existing property"""
    property_instance = get_object_or_404(Property, id=property_id)
    
    # Optional: Check if user is the owner
    # if property_instance.agent != request.user:
    #     messages.error(request, 'You do not have permission to edit this property.')
    #     return redirect('property_list')
    
    if request.method == 'POST':
        try:
            # Get price value, use property_price if price is not provided
            price_value = request.POST.get('price')
            if not price_value:
                price_value = request.POST.get('property_price')
            
            # Update property fields
            property_instance.property_type = request.POST.get('property_type')
            property_instance.property_status = request.POST.get('property_status')
            property_instance.property_price = request.POST.get('property_price')
            property_instance.max_rooms = request.POST.get('max_rooms')
            property_instance.beds = request.POST.get('beds')
            property_instance.baths = request.POST.get('baths')
            property_instance.area = request.POST.get('area')
            property_instance.price = price_value
            property_instance.premiere = request.POST.get('premiere')
            property_instance.description = request.POST.get('description', '')
            property_instance.address = request.POST.get('address')
            property_instance.zip_code = request.POST.get('zip_code')
            property_instance.city = request.POST.get('city')
            property_instance.state = request.POST.get('state')
            property_instance.country = request.POST.get('country')
            
            property_instance.save()
            
            # Handle new image uploads
            images = request.FILES.getlist('property_images')
            if images:
                for image in images:
                    PropertyImage.objects.create(
                        property=property_instance,
                        image=image,
                        is_primary=False  # Don't make new images primary automatically
                    )
            
            messages.success(request, f'Property {property_instance.property_id} updated successfully!')
            return redirect('property_details_id', property_id=property_instance.id)
            
        except Exception as e:
            messages.error(request, f'Error updating property: {str(e)}')
    
    context = {
        'page_title': f'Edit Property - {property_instance.property_id}',
        'property': property_instance
    }
    return render(request, 'products/add_property.html', context)


@login_required
def delete_property(request, property_id):
    """View to delete a property"""
    property_instance = get_object_or_404(Property, id=property_id)
    
    # Optional: Check if user is the owner
    # if property_instance.agent != request.user:
    #     messages.error(request, 'You do not have permission to delete this property.')
    #     return redirect('property_list')
    
    if request.method == 'POST':
        property_id_display = property_instance.property_id
        property_instance.delete()
        messages.success(request, f'Property {property_id_display} deleted successfully!')
        return redirect('property_list')
    
    context = {
        'page_title': f'Delete Property - {property_instance.property_id}',
        'property': property_instance
    }
    return render(request, 'products/delete_property.html', context)


@login_required
def add_property_feature(request, property_id):
    """View to add features to a property"""
    property_instance = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        feature_name = request.POST.get('feature_name')
        if feature_name:
            PropertyFeature.objects.create(
                property=property_instance,
                feature_name=feature_name
            )
            messages.success(request, f'Feature "{feature_name}" added successfully!')
        else:
            messages.error(request, 'Please enter a feature name.')
        return redirect('property_details_id', property_id=property_id)
    
    context = {
        'property': property_instance
    }
    return render(request, 'products/add_feature.html', context)