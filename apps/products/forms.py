from django import forms
from .models import Property, PropertyImage, PropertyFeature


class PropertyForm(forms.ModelForm):
    """Form for creating and editing properties"""
    
    class Meta:
        model = Property
        fields = [
            'property_type', 'property_status', 'property_price',
            'max_rooms', 'beds', 'baths',
            'area', 'price', 'premiere',
            'description',
            'address', 'zip_code', 'city', 'state', 'country',
            'property_size', 'garage', 'garage_size', 'year_built',
            'is_featured'
        ]
        
        widgets = {
            'property_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'office,villa,apartment'
            }),
            'property_status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'property_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': '$2800'
            }),
            'max_rooms': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'beds': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'baths': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'area': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': '85 sq ft'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': '$3000'
            }),
            'premiere': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary resize-none',
                'rows': 4
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Address of your property'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter pin code'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter state'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter country'
            }),
        }


class PropertyImageForm(forms.ModelForm):
    """Form for uploading property images"""
    
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_primary', 'caption']
        
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'multiple': True
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-border rounded-lg',
                'placeholder': 'Image caption'
            }),
        }


class PropertyFeatureForm(forms.ModelForm):
    """Form for adding property features"""
    
    class Meta:
        model = PropertyFeature
        fields = ['feature_name']
        
        widgets = {
            'feature_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-border rounded-xl bg-bg text-text focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Feature name (e.g., Air Conditioning)'
            }),
        }


# Multiple Image Upload Form
class MultipleImageUploadForm(forms.Form):
    """Form for uploading multiple images at once"""
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            'accept': 'image/*',
            'class': 'hidden'
        }),
        required=False
    )