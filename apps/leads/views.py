from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.utils.timezone import now
from django.core.paginator import Paginator
from .models import Lead
from django.contrib import messages
from django.db.models import Q, Case, When, IntegerField, BooleanField
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
import datetime
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.urls import reverse

User = get_user_model()



# agent leads can see only own leads 
@login_required(login_url='login')
def agent_leads(request):
    search_query = request.GET.get("q", "").strip()
    current_time = now()

    base_qs = Lead.objects.filter(assigned_agent=request.user).exclude(status="closed")

    followups = base_qs.filter(
        follow_up_at__isnull=False,
        follow_up_at__lte=current_time
    )

    upcoming_followups = base_qs.filter(
        follow_up_at__isnull=False,
        follow_up_at__gt=current_time
    ).order_by("follow_up_at")

    leads_qs = base_qs

    if search_query:
        leads_qs = leads_qs.filter(name__icontains=search_query)

    leads_qs = leads_qs.annotate(
        is_due=Case(
            When(
                follow_up_at__isnull=False,
                follow_up_at__lte=current_time,
                then=True
            ),
            default=False,
            output_field=BooleanField()
        )
    ).order_by(
        "-is_due",
        "-updated_at"
    )

    paginator = Paginator(leads_qs, 10)
    # try:
    leads = paginator.get_page(request.GET.get("page"))
    
    # exception as  e
    context = {
        "page_title": "My Leads",
        "leads": leads,
        "followups": followups,
        "upcoming_followups": upcoming_followups,
        "search_query": search_query,
    }

    return render(request, "agents/agents_leads.html", context)





# upate the lead in agent only
@login_required
@permission_required("leads.can_update_lead", raise_exception=True)
def update_lead_status(request, lead_id):

    lead = get_object_or_404(Lead, id=lead_id)
    user = request.user

    if not (
        user.is_staff or
        lead.assigned_agent == user or
        lead.assigned_associate == user
    ):
        raise Http404("Not allowed")

    if request.method == "POST":
        lead.status = request.POST.get("status")
        lead.property_type = request.POST.get("property_type") or ""
        lead.preferred_location = request.POST.get("preferred_location") or ""
        lead.budget_min = request.POST.get("budget_min") or None
        lead.budget_max = request.POST.get("budget_max") or None
        lead.purchase_timeline = request.POST.get("purchase_timeline") or ""

        lead.interest_level = request.POST.get("interest_level") or ""
        lead.next_action = request.POST.get("next_action") or ""
        lead.client_response = request.POST.get("client_response") or ""
        lead.objections = request.POST.get("objections") or ""

        follow_up = request.POST.get("follow_up_at")
        if follow_up:
            dt = parse_datetime(follow_up)
            if dt and settings.USE_TZ:
                dt = make_aware(dt)
            lead.follow_up_at = dt
        else:
            lead.follow_up_at = None

        lead.agent_note = request.POST.get("agent_note") or ""
        lead.save()

        # redirect based on role
        if user.is_staff:
            return redirect("admin_leads")
        # elif user.role == "associate":
        #     return redirect('associate_leads')
        else:
            return redirect("agent_leads")

    return render(request,"agents/update_status.html",
        {"lead": lead,'page_title':'Updated_Details'}
    )


# admin leads 

@staff_member_required
def admin_leads(request):

    today = now().date()
    date_filter = request.GET.get("date", "")
    agent_id = request.GET.get("agent", "")
    leads = Lead.objects.select_related("assigned_agent")


    if date_filter == "today":
        leads = leads.filter(assigned_at__date=today)
    
    elif date_filter == "yesterday":
        start = today - datetime.timedelta(days = 1)
        end = today
        leads = leads.filter(assigned_at__date__gte=start,assigned_at__date__lt=end)

    elif date_filter == "week":
        start_week = today - datetime.timedelta(days=7)
        leads = leads.filter(assigned_at__date__gte=start_week)

    
    if agent_id:
        try:
            agent = User.objects.get(pk=int(agent_id))   
            leads = leads.filter(assigned_agent=agent)  
        except (ValueError, User.DoesNotExist):
            messages.error(request, "Selected agent does not exist")

    stats = {
        "total": leads.count(),
        "open": leads.exclude(status="closed").count(),
        "closed": leads.filter(status="closed").count(),
    }


    agents = User.objects.filter(
        id__in=Lead.objects.values_list("assigned_agent_id", flat=True)
    ).distinct()

    context = {
        "page_title": "All Leads",
        "leads": leads.order_by("-updated_at"),
        "stats": stats,
        "agents": agents,
        "date_filter": date_filter,
        "agent_id": agent_id,
    }

    return render(request, "admin/admin_leads.html", context)



# submit the lead 

def submit_lead(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        agents = User.objects.filter(is_staff=False, is_active=True)

        agent = min(agents,key=lambda a: Lead.objects.filter(assigned_agent=a).count(),default=None)

        Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            assigned_agent=agent,
            assigned_at=now()
        )

        return redirect("lead_success")

    return render(request,"public/submit_lead.html",{"page_title": "Submit Lead"})


# lead sucess message
def lead_success(request):
    return render(request,"public/sucess.html",{"page_title": "Success"})



# delete leads
@login_required
@permission_required("leads.can_delete_lead", raise_exception=True)
def delete_lead(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id,
        assigned_agent=request.user   
    )

    if request.method == "POST":
        lead.delete()
        return redirect("agent_leads")
    return render(request,"agents/confirm_delete.html",{"lead": lead})



# agent can see the all details in the user

def lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    user = request.user

 
    if not (
        user.is_staff or
        lead.assigned_agent == user or
        lead.assigned_associate == user
    ):
        raise Http404("Not allowed")

   
    if user.is_staff:
        default_back = reverse("admin_leads")
    elif user.role == "associate":
        default_back = reverse("agent_dashboard")  
    else:
        default_back = reverse("agent_leads")      

    back_url = request.META.get("HTTP_REFERER", default_back)

    return render(request,"agents/lead_details.html",
        {
            "lead": lead,
            "back_url": back_url,
            "page_title": "Details"
        }
    )



@login_required
@permission_required("leads.can_book_lead", raise_exception=True)
def booking_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    return render(request, "agents/booking.html", {"lead": lead})





# admin can be give the permisions to the agent
@login_required
def manage_permissions(request, user_id):

    if not request.user.is_superuser:
        return redirect("agent_dashboard")

    agents = User.objects.exclude(role=User.Role.SUPERUSER)

    selected_agent = None
    permissions = []
    user_permissions = []

    lead_ct = ContentType.objects.get(app_label="leads", model="lead")


    agent_id = request.GET.get("agent")
    if agent_id:
        selected_agent = get_object_or_404(User, id=agent_id)

        permissions = Permission.objects.filter(
            content_type=lead_ct,
            codename__in=[
                "can_update_lead",
                "can_delete_lead",
                "can_book_lead",
            ]
        )

        user_permissions = selected_agent.user_permissions.values_list(
            "id", flat=True
        )

    if request.method == "POST":
        agent_id = request.POST.get("agent_id")
        selected_agent = get_object_or_404(User, id=agent_id)

        selected_permissions = request.POST.getlist("permissions")

        selected_agent.user_permissions.clear()
        selected_agent.user_permissions.add(*selected_permissions)

        return redirect("manage_permissions", user_id=user_id)
 
    return render(request,"admin_dash/manage_permissions.html",
        {
            "agents": agents,
            "selected_agent": selected_agent,
            "permissions": permissions,
            "user_permissions": user_permissions,
            "page_title":"Permissions",
        }
    )
    
    
    
# shedule lead

@login_required
def schedule_lead(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id,
        assigned_agent=request.user
    )

    if request.method == "POST":
        lead.site_visit_at = request.POST.get("follow_up_at")
        lead.status = "New"
        lead.save()


        return redirect("agent_leads")

    return render(request,"agents/set_shedule.html",
        {
            "lead": lead,
            "page_title": "Schedule Site Visit"
        }
    )


    
    
    


# assigned the task for associates

@login_required
def move_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.user != lead.assigned_agent:
        return redirect("agent_leads")

    associates = User.objects.filter(
        role="associate",
        parent_agent=request.user
    )

    if request.method == "POST":
        associate_id = request.POST.get("associate")
        associate = get_object_or_404(
            User,
            id=associate_id,
            parent_agent=request.user
        )

        lead.assigned_associate = associate
        lead.save()

        return redirect("agent_leads")

    return render(request, "agents/move_lead.html", {
        "lead": lead,
        "associates": associates,
        'page_title':'move lead',
    })



# associate_leads

@login_required
def associate_leads(request):
    user = request.user

    # Safety check
    if user.role != "associate":
        return redirect("associate_leads")

    leads = Lead.objects.filter(
        assigned_associate=user
    ).order_by("-updated_at")

    return render(request,"associates/associate_leads.html",
        {
            "leads": leads,
            'page_title':'My Leads'
        }
    )
