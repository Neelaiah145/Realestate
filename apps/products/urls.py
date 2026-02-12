from django.urls import path
from .views import property_list,property_create,property_update,property_delete,about_property
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("properties/", property_list, name="property_list"),
    path("properties/create/", property_create, name="property_create"),
    path("properties/<int:pk>/update/", property_update, name="property_update"),
    path("properties/<int:pk>/delete/", property_delete, name="property_delete"),
    path("properties/<int:pk>/about/", about_property, name="about_property"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)