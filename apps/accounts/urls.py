from django.urls import path
from .views import login_view,logout_view,admin_dashboard_view,change_superuser_image,base,toggle_user_status,delete_user,base,agent_dashboard_view

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_dashboard/',admin_dashboard_view,name='admin_dashboard'),
    path('superuser/change-image/', change_superuser_image, name="change_superuser_image"),
    path('base/',base,name='base'),
    path("user/status/<int:user_id>/", toggle_user_status, name="toggle-user"),
    path("user/delete/<int:user_id>/", delete_user, name="delete-user"),
    path('agents/agent_dashboard/',agent_dashboard_view,name='agent_dashboard'),
    
    
]
