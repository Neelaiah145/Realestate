from django.urls import path
from .views import admin_leads,agent_leads

urlpatterns = [
 
    path('agent_leads/',agent_leads,name = 'agent_leads'),
    path('admin_leads/',admin_leads,name = 'admin_leads'),
    
]