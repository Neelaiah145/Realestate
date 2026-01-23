from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import os
User = get_user_model()
# =========================
# REDIRECT BASED ON USER
# =========================
def redirect_user(user):
    if user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('agent_dashboard')


# =========================
# LOGIN VIEW (NO login_required)
# =========================
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


# =========================
# DASHBOARDS
# =========================
# @login_required
# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')


# @login_required
# def user_dashboard(request):
#     return render(request, 'pages/analytics.html')


# =========================
# LOGOUT
# =========================

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








# ====================================================================================================
# admin dashboard 
@login_required
def admin_dashboard_view(request):
    user = request.user

    if user.is_superuser:
        users = User.objects.exclude(role=User.Role.SUPERUSER)
    else:
        users = None  # agents cannot see others

    if request.method == "POST" and user.is_superuser:
        User.objects.create_user(
            email=request.POST["email"],
            password=request.POST["password"],
            username=request.POST["username"],
            phone=request.POST.get("phone"),
            role=request.POST["role"]
        )
        messages.success(request, "User created successfully")
        return redirect("admin_dashboard")

    context = {
        "users": users,
        "is_admin": user.is_superuser
    }

    return render(request, "admin_dash/admin_dashboard.html", context)



@login_required
def agent_dashboard_view(request):
    return render(request,'agent/agent_dashboard.html')



# @login_required
# def analytics(request):
#     return render(request,'pages/analytics.html',{'page_title':'Analytics'})



# used for toggle mean status in agent/associate
@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        return redirect("admin_dashboard")

    u = get_object_or_404(User, id=user_id)
    u.is_active = not u.is_active
    u.save()
    return redirect("admin_dashboard") 




# delete the agent/associate in admin page
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("admin_dashboard")

    get_object_or_404(User, id=user_id).delete()
    return redirect("admin_dashboard")



# base file for html code to use all html files

def base(request):
    return render(request,'base.html')





# def login_view(request):
#     print("hai")
#     return render(request,'accounts/login.html')



