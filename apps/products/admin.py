from django.contrib import admin
from .models import Property, PropertyImage, PropertyFeature, PropertyLocation


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'is_primary', 'caption')


class PropertyFeatureInline(admin.TabularInline):
    model = PropertyFeature
    extra = 1
    fields = ('feature_name',)


class PropertyLocationInline(admin.StackedInline):
    model = PropertyLocation
    extra = 0
    fields = ('latitude', 'longitude', 'area_name')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # FIXED: Added 'is_featured' to list_display
    list_display = ('property_id', 'property_type', 'property_status', 'property_price', 'city', 'state', 'agent', 'is_featured', 'created_at')
    list_filter = ('property_status', 'property_type', 'city', 'state', 'is_featured')
    search_fields = ('property_id', 'address', 'city', 'state', 'zip_code')
    list_editable = ('property_status', 'is_featured')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('property_type', 'property_status', 'property_price', 'property_id')
        }),
        ('Room Details', {
            'fields': ('max_rooms', 'beds', 'baths')
        }),
        ('Property Details', {
            'fields': ('area', 'price', 'premiere', 'description', 'property_size', 'garage', 'garage_size', 'year_built')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'zip_code')
        }),
        ('Agent & Status', {
            'fields': ('agent', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PropertyImageInline, PropertyFeatureInline, PropertyLocationInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.agent:
            obj.agent = request.user
        super().save_model(request, obj, form, change)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('property__property_id', 'caption')


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ('property', 'feature_name')
    search_fields = ('property__property_id', 'feature_name')


@admin.register(PropertyLocation)
class PropertyLocationAdmin(admin.ModelAdmin):
    list_display = ('property', 'area_name', 'latitude', 'longitude')
    search_fields = ('property__property_id', 'area_name')