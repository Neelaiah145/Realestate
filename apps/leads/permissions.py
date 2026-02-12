from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .views import *




@login_required
def manage_permissions(request, user_id):

    agents = User.objects.exclude(is_superuser=True)

    selected_agent = None
    permissions = []
    user_permissions = []

    dashboard_ct = ContentType.objects.get(app_label = "accounts",model = "user")
    lead_ct = ContentType.objects.get(app_label="leads", model="lead")
    account_ct = ContentType.objects.get(app_label="accounts", model="user")
    property_ct = ContentType.objects.get(app_label = "products",model = "property")
    contacts_ct = ContentType.objects.get(app_label = "leads", model = "lead")

    #  MANUAL MENU CONFIG (IMPORTANT)
    MENU_CONFIG = [
        
        
            # dahboard
        {
            "key":"dashboard",
            "menu_codename":"view_dashboard",
            "children":[],
        },
        
           # agents create page
        {
            "key": "associate",
            "menu_codename": "view_create_associate",
            "children": [],  
        },
        
        
            # leads
        {
            "key": "leads",
            "menu_codename": "view_leads",
            "children": [
                "can_update_lead",
                "can_delete_lead",
                "can_book_lead",
            ],

        },

            # products
        {
            "key":"property",
            "menu_codename":"view_property",
            "children":[
                "add_property",
                "change_property",
                "delete_property",
            ],
        },
        
        # contacts
                {
            "key":"contacts",
            "menu_codename":"view_contacts",
            "children":[
                "change_contact",
                "delete_contact",
            ],
        },
            
            
            
            
            
            # other
            
            
            
        
    ]

    agent_id = request.GET.get("agent")
    if agent_id:
        selected_agent = get_object_or_404(User, id=agent_id)

        permissions = Permission.objects.filter(
            Q(
                content_type=lead_ct,
                codename__in=[
                    "view_leads",
                    "can_update_lead",
                    "can_delete_lead",
                    "can_book_lead",
                ]
            )
            |
            Q(
                content_type=account_ct,
                codename__in=["view_create_associate"]
            )
            |
            Q(
                content_type=dashboard_ct,
                codename__in=["view_dashboard"]
            )
            |
            Q(
                content_type=property_ct,
                codename__in=["view_property",
                              "add_property",
                              "change_property",
                              "delete_property",
                            ]
            )
            |
            Q(
                content_type=contacts_ct ,
                codename__in=["view_contacts",
                              "change_contact",
                              "delete_contact",
                              
                            ]
            )
            
            
            
        ).order_by("content_type__app_label", "codename")

        user_permissions = selected_agent.user_permissions.values_list(
            "id", flat=True
        )

    if request.method == "POST":
        selected_agent = get_object_or_404(User, id=request.POST.get("agent_id"))
        selected_permissions = request.POST.getlist("permissions")

        selected_agent.user_permissions.remove(*permissions)
        selected_agent.user_permissions.add(*selected_permissions)

        return redirect(f"{request.path}?agent={selected_agent.id}")

    return render(
        request,
        "admin/manage_permissions.html",
        {
            "agents": agents,
            "selected_agent": selected_agent,
            "permissions": permissions,
            "user_permissions": user_permissions,
            "menu_config": MENU_CONFIG,  
            "page_title": "Permissions",
           
        }
    )

        
        
    
 
        
        
        
        
          

 
  