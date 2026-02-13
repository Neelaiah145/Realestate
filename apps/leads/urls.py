from django.urls import path
from .views import admin_leads,agent_leads,submit_lead,lead_success,agent_leads,update_lead_status,delete_lead,lead_detail,booking_lead
from .views import schedule_lead,move_lead,associate_leads,contacts,delete_contact,edit_contact
from apps.leads.permissions import manage_permissions,create_lead_admin
urlpatterns = [
 
    path('agent_leads/',agent_leads,name = 'agent_leads'),
    path('admin_leads/',admin_leads,name = 'admin_leads'),
    path("submit_lead/", submit_lead, name="submit_lead"),
    path("success_lead/", lead_success, name="lead_success"),
    path("agent_status/<int:lead_id>/", update_lead_status, name="update_lead_status"),
    path("agent/delete/<int:lead_id>/",delete_lead,name="delete_lead"),
    path("agent/lead/<int:lead_id>/",lead_detail,name="lead_detail"),
    path("booking/",booking_lead,name="booking"),
    path("admin/user/<int:user_id>/manage_permissions/",manage_permissions,name="manage_permissions"),
    path('set_shedule/<int:lead_id>/',schedule_lead,name='set_shedule'),
    path('lead/<int:lead_id>/move_lead/',move_lead,name='move_lead'),
    path('associate/associate_leads/',associate_leads,name = 'associate_leads'),
    path('contacts/',contacts,name = 'contacts'),
    path('delete_contact/<int:id>/',delete_contact,name='delete_contact'),
    path('edit_contact/<int:id>/',edit_contact,name = 'edit_contact'),
    path('create_lead_by_admin/',create_lead_admin,name="create_lead_admin"),
    
    


  
    
]