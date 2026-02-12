from django.urls import path
from .views import login_view,logout_view,admin_create_agent_view,change_superuser_image,toggle_user_status,delete_user,agent_create_ass_view
from .views import associate_dashboard_view,base,admin_dashboard,agent_dashboard,send_otp,verify_otp,otp_form,admin_update_agent_view,admin_delete_agent_view
from .views import toggle_agent_status

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_create_agent/',admin_create_agent_view,name='admin_create_agent'),
    path('superuser/change-image/', change_superuser_image, name="change_superuser_image"),
    path('base/',base,name='base'),
    path("user/status/<int:user_id>/", toggle_user_status, name="toggle-user"),
    path("user/delete/<int:user_id>/", delete_user, name="delete-user"),
    path('agent_create_ass/',agent_create_ass_view,name='agent_create_ass'),
    path('associate_dashboard/',associate_dashboard_view,name='associate_dashboard'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('agent_dashboard/',agent_dashboard,name='agent_dashboard'),
    path("send-otp/", send_otp, name="send_otp"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path('otp_form/',otp_form,name="otp_form"),
    path("agent_edit/<int:user_id>/",admin_update_agent_view,name ="admin_update_agent_view"),
    path("agent_delete/<int:user_id>/",admin_delete_agent_view,name ="admin_delete_agent_view"),
    path("user_status/<int:user_id>/",toggle_agent_status,name='associate_status'),
    


    
    

    
    
    
]
