from django.db import models
from django.conf import settings

class Property(models.Model):
    PROPERTY_STATUS_CHOICES = [
        ('for_rent', 'For Rent'),
        ('for_sale', 'For Sale'),
        ('sold', 'Sold'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('office', 'Office'),
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
    ]
    
    # Basic Information
    property_type = models.CharField(max_length=100)
    property_status = models.CharField(max_length=20, choices=PROPERTY_STATUS_CHOICES, default='for_rent')
    property_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Room Details
    max_rooms = models.IntegerField(default=1)
    beds = models.IntegerField(default=1)
    baths = models.IntegerField(default=1)
    
    # Property Details
    area = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    premiere = models.CharField(max_length=100)
    
    # Description
    description = models.TextField(blank=True, null=True)
    
    # Location
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Additional Details
    property_id = models.CharField(max_length=50, unique=True, blank=True)
    property_size = models.CharField(max_length=50, blank=True)
    garage = models.IntegerField(default=0)
    garage_size = models.CharField(max_length=50, blank=True)
    year_built = models.IntegerField(blank=True, null=True)
    
    # Agent
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Featured
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.property_type} - {self.address}"
    
    def save(self, *args, **kwargs):
        if not self.property_id:
            # Get all existing property IDs and extract the numeric part
            existing_ids = Property.objects.all().values_list('property_id', flat=True)
            
            # Extract numbers from property IDs (e.g., "RT1" -> 1, "RT5" -> 5)
            existing_numbers = []
            for prop_id in existing_ids:
                if prop_id and prop_id.startswith('RT'):
                    try:
                        num = int(prop_id.replace('RT', ''))
                        existing_numbers.append(num)
                    except ValueError:
                        continue
            
            # Find the next available number
            if existing_numbers:
                # Start from 1 and find the first missing number
                existing_numbers.sort()
                next_num = 1
                for num in existing_numbers:
                    if num == next_num:
                        next_num += 1
                    elif num > next_num:
                        break
                self.property_id = f"RT{next_num}"
            else:
                # No properties exist, start with RT1
                self.property_id = "RT1"
        
        super().save(*args, **kwargs)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.property.property_id}"


class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.feature_name


class PropertyLocation(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='location_details')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    area_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Location for {self.property.property_id}"