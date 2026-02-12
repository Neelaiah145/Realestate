from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apps.leads.models import Lead
from .models import OTP
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta
from .utils import send_smslogin_otp
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.core.paginator import Paginator


import os
User = get_user_model()


# REDIRECT BASED ON USER

def redirect_user(user):
    if user.is_superuser:
        return redirect('admin_dashboard')

    elif user.role == 'associate':
        return redirect('associate_dashboard')

    else:
        return redirect('agent_dashboard')


# LOGIN VIEW (NO login_required)

def login_view(request):
    if request.user.is_authenticated:
        return redirect_user(request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect_user(user)
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'accounts/login.html')



# DASHBOARDS

# @login_required
# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')


# @login_required
# def user_dashboard(request):
#     return render(request, 'pages/analytics.html')



# LOGOUT


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# chanage the images
@login_required
def change_superuser_image(request):
    if not request.user.is_superuser:
        return redirect("admin_dashboard")
    if request.method == "POST" and request.FILES.get("profile_image"):
        user = request.user
        if user.profile_image:
            old_path = user.profile_image.path
            if os.path.exists(old_path):
                os.remove(old_path)       
        user.profile_image = request.FILES["profile_image"]
        user.save()
    return redirect("admin_dashboard")








# admin dashboard 
@login_required
def admin_create_agent_view(request):
    user = request.user

    users = User.objects.none()
    search_query = request.GET.get("q", "")
    role_filter = request.GET.get("role", "")

    if user.is_superuser:
        users = User.objects.exclude(role=User.Role.SUPERUSER)

        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        if role_filter:
            users = users.filter(role=role_filter)

    
    paginator = Paginator(users, 3) 
    page_number = request.GET.get("page")
    users_page = paginator.get_page(page_number)

    if request.method == "POST" and user.is_superuser:
        User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"],
            phone=request.POST.get("phone"),
            role=request.POST["role"]
        )
        messages.success(request, "User created successfully")
        return redirect("admin_create_agent")

    context = {
        "users": users_page,    
        "is_admin": user.is_superuser,
        "search_query": search_query,
        "role_filter": role_filter,
        "page_title": "Agent_Creation",
    }

    return render(request, "admin_dash/admin_create_agent.html", context)




# update/edit  agent details


@login_required
def admin_update_agent_view(request, user_id):

    if not request.user.is_superuser:
        messages.error(request, "You are not authorized.")
        return redirect("admin_create_agent")

    agent = get_object_or_404(User, id=user_id)

    if request.method == "POST":

        agent.username = request.POST.get("username")
        agent.phone = request.POST.get("phone")
        password = request.POST.get("password")

        if password:
            agent.set_password(password)

        agent.save()

        messages.success(request, "Agent updated successfully")
        return redirect("admin_create_agent")

    context = {
        "agent": agent,
        "page_title": "Edit Agent",
    }

    return render(request, "admin_dash/edit.html", context)



# delete agent

@login_required
def admin_delete_agent_view(request, user_id):

    if not request.user.is_superuser:
        return redirect("admin_create_agent")

    agent = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        agent.delete()
        return redirect("admin_create_agent")

    return render(request, "admin_dash/agent_delete.html", {
        "agent": agent
    })

    

# creat and all users

# def admin_create_agent_view(request):
#     user = request.user

#     users = None
#     search_query = request.GET.get("q", "")
#     role_filter = request.GET.get("role", "")

#     if user.is_superuser:
#         users = User.objects.exclude(role=User.Role.SUPERUSER)\
#                             .select_related("reporting_agent")

#         #  Search
#         if search_query:
#             users = users.filter(
#                 Q(username__icontains=search_query) |
#                 Q(email__icontains=search_query)
#             )

#         #  Role filter
#         if role_filter:
#             users = users.filter(role=role_filter)

#     #  Create user
#     if request.method == "POST" and user.is_superuser:
#         role = request.POST["role"]
#         reporting_agent_id = request.POST.get("reporting_agent")

#         reporting_agent = None
#         if role == User.Role.ASSOCIATE and reporting_agent_id:
#             reporting_agent = User.objects.get(id=reporting_agent_id)

#         User.objects.create_user(
#             username=request.POST["username"],
#             email=request.POST["email"],
#             password=request.POST["password"],
#             phone=request.POST.get("phone"),
#             role=role,
#             reporting_agent=reporting_agent
#         )

#         messages.success(request, "User created successfully")
#         return redirect("admin_create_agent")

#     context = {
#         "users": users,
#         "agents": User.objects.filter(role=User.Role.AGENT),
#         "is_admin": user.is_superuser,
#         "search_query": search_query,
#         "role_filter": role_filter,
#         "page_title": "Admin_Page"
#     }

#     return render(request, "admin_dash/admin_create_agent.html", context)


# end for all usrs and create










from django.http import HttpResponseForbidden
@login_required
@permission_required('accounts.view_create_associate',raise_exception=True)
def agent_create_ass_view(request):
    user = request.user


    # CREATE associate
    if request.method == "POST" and user.role == "agent":
        User.objects.create_user(
            email=request.POST["email"],
            username=request.POST["username"],
            password=request.POST["password"],
            role="associate",
            parent_agent=user
        )
        return redirect("agent_create_ass")


    associates = User.objects.filter(
        role="associate",
        parent_agent=user
    )

    return render(request,"agent/agent_create_ass.html",
        {"associates": associates,'page_title':'Create_Associate'}
    )


# @login_required
# def analytics(request):
#     return render(request,'pages/analytics.html',{'page_title':'Analytics'})



# used for toggle mean status in agent (active/diactive)

@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        return redirect("admin_create_agent")

    u = get_object_or_404(User, id=user_id)
    u.is_active = not u.is_active
    u.save()
    return redirect("admin_create_agent") 


# used for toggle mean status in associate (active/diactive)
@login_required
def toggle_agent_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    user.is_active = not user.is_active
    user.save()
    
    return redirect("agent_create_ass")


# delete the agent/associate in admin page
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("admin_create_agent")

    get_object_or_404(User, id=user_id).delete()
    return redirect("admin_create_agent")



# base file for html code to use all html files

def base(request):
    return render(request,'base.html')





# def login_view(request):
#     print("hai")
#     return render(request,'accounts/login.html')


def phone_login_view(request):
    return render(request, "accounts/login_phone.html")



# otp send view
from django.http import JsonResponse
import random
from .utils import send_smslogin_otp

def send_otp(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    phone = request.POST.get("phone", "").strip()

    if not phone:
        return JsonResponse({"error": "Phone required"}, status=400)

   
    phone = phone.replace("+", "").replace(" ", "")
    phone = phone[-10:]  

   
    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={
            "username": phone  
        }
    )

    otp = random.randint(1000, 9999)

    OTP.objects.filter(user=user, is_verified=False).update(is_verified=True)
    OTP.objects.create(
        user=user,
        phone=phone,
        otp=str(otp)
    )

    request.session["otp_user_id"] = user.id

    send_smslogin_otp(phone, otp)
    print("otp sended :", otp)

    return JsonResponse({"success": True})



# verify otp
def verify_otp(request):
    user_id = request.session.get("otp_user_id")

    if not user_id:
        return redirect("login")

    if request.method == "POST":
        otp_input = request.POST.get("otp", "").strip()

        otp_obj = OTP.objects.filter(
            user_id=user_id,
            is_verified=False
        ).order_by("-created_at").first()

        if not otp_obj or otp_obj.otp != otp_input:
            return redirect("otp_form")

        if now() - otp_obj.created_at > timedelta(minutes=5):
            return redirect("login")

        otp_obj.is_verified = True
        otp_obj.save()

        login(
            request,
            otp_obj.user,
            backend="django.contrib.auth.backends.ModelBackend"
        )

        request.session.pop("otp_user_id", None)

        return redirect_user(otp_obj.user)

    return redirect("login")






def otp_form(request):
    return render(request,'accounts/otp_form.html')





# def associate_base(request):
#     return render(request,'associate_base.html')

from apps.accounts.analytics import monthly_analytics,lead_status_analytics
@permission_required("accounts.view_dashboard", raise_exception=True)
@login_required
def admin_dashboard(request):
    leads = Lead.objects.all()
    role = User.objects.all()
    chart = monthly_analytics()
    status_chart = lead_status_analytics()
    # count the users
    stats = {
        "total":leads.count(),
        "agents":role.filter(role = 'agent').count(),
        "associates":role.filter(role = "associate").count()
    }
    
    context = {
        'stats':stats,
         "chart": chart,
         "status_chart":status_chart
    }
    return render(request,'admin_dash/admin_dashboard.html',context)




@login_required
def agent_dashboard(request):
    current_time = now()
    
    leads = Lead.objects.filter(assigned_agent=request.user).exclude(status="closed")
    status_counts = {
        "new": Lead.objects.filter(assigned_agent=request.user, status="new").count(),
        "contacted": Lead.objects.filter(assigned_agent=request.user, status="contacted").count(),
        "closed": Lead.objects.filter(assigned_agent=request.user, status="closed").count(),
        "intersted":Lead.objects.filter(assigned_agent=request.user, status="intersted").count(),
        }
    base_qs = Lead.objects.filter(assigned_agent=request.user).exclude(status="closed")
    
    followups = base_qs.filter(
    follow_up_at__isnull=False,
    follow_up_at__lte=current_time
    )
    content = {
        'leads':leads,
        "status_counts":status_counts,
        "followups":followups 
       
    }

    return render(request, "agent/agent_dashboard.html",content)


@login_required
def associate_dashboard_view(request):

    return render(request,"associate/associate_dashboard.html",)



def otp_forms(request):
    return render(request,'accounts/otp_form.html')





# give dashboard permison

