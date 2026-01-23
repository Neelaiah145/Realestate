from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.utils.timezone import now
from django.core.paginator import Paginator
from .models import Lead
from django.db.models import Q, Case, When, IntegerField, BooleanField
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
import datetime
import csv
User = get_user_model()



# agent leads can see only own leads 

@login_required
def agent_leads(request):
    search_query = request.GET.get("q", "").strip()
    current_time = now()
    base_qs = Lead.objects.filter(
        assigned_agent=request.user
    ).exclude(status="closed")
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
    leads = paginator.get_page(request.GET.get("page"))
    return render(request,"agents/agents_leads.html",
        {"leads": leads,"followups": followups,"upcoming_followups": upcoming_followups,"search_query": search_query,})




# upate the lead in agent only
@login_required
def update_lead_status(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id,
        assigned_agent=request.user
    )
    if request.method == "POST":
        lead.status = request.POST.get("status")
        lead.agent_note = request.POST.get("agent_note")

        follow_up = request.POST.get("follow_up_at")

        follow_up = request.POST.get("follow_up_at")
        if follow_up:
            dt = parse_datetime(follow_up)
            if dt and settings.USE_TZ:
                dt = make_aware(dt)
        lead.follow_up_at = dt
        lead.save()
        return redirect("agent_leads")

    return render(request,"agents/update_status.html",{"lead": lead})





# admin leads 
@staff_member_required
def admin_leads(request):
    today = now().date()
    date_filter = request.GET.get("date", "")
    agent_id = request.GET.get("agent", "")
    leads = Lead.objects.select_related("assigned_agent")

    if date_filter == "today":
        leads = leads.filter(assigned_at__date=today)

    elif date_filter == "week":
        start_week = today - datetime.timedelta(days=7)
        leads = leads.filter(assigned_at__date__gte=start_week)

    if agent_id.isdigit():
        leads = leads.filter(assigned_agent_id=int(agent_id))
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
@login_required
def lead_detail(request, lead_id):
    lead = get_object_or_404(
        Lead,
        id=lead_id,
        assigned_agent=request.user   
    )

    return render(request,"agents/lead_details.html",{"lead": lead})



