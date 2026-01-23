from django.urls import path
from . import views

urlpatterns = [
    # Property URLs
    path('property/add/', views.add_property, name='add_property'),
    path('property/list/', views.property_list, name='property_list'),
    path('property/details/', views.property_details, name='property_details'),
    path('property/details/<int:property_id>/', views.property_details, name='property_details_id'),
    path('property/edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('property/delete/<int:property_id>/', views.delete_property, name='delete_property'),
    path('property/<int:property_id>/add-feature/', views.add_property_feature, name='add_property_feature'),
]