from django.urls import path
from .views import admin_leads,agent_leads,submit_lead,lead_success,agent_leads,update_lead_status

urlpatterns = [
 
    path('agent_leads/',agent_leads,name = 'agent_leads'),
    path('admin_leads/',admin_leads,name = 'admin_leads'),
    path("submit_lead/", submit_lead, name="submit_lead"),
    path("success_lead/", lead_success, name="lead_success"),
    path("agent_status/<int:lead_id>/", update_lead_status, name="update_lead_status"),
  
    
]