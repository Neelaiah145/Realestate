from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.utils.timezone import now
from .models import Lead
from django.contrib.auth import get_user_model
User = get_user_model()


# agent leads can see only own leads 
@login_required
def agent_leads(request):
    leads = Lead.objects.filter(assigned_agent=request.user)

    context = {
        "page_title": "My Leads",
        "leads": leads,}

    return render(request,"agents/agents_leads.html",context)


# upate the lead in agent only
@login_required
def update_lead_status(request, lead_id):
    lead = get_object_or_404(Lead,id=lead_id,assigned_agent=request.user
    )

    if request.method == "POST":
        lead.status = request.POST.get("status")
        lead.save()
        return redirect("agent_leads")

    context = {
        "page_title": "Update Lead Status",
        "lead": lead,
    }

    return render(request,"agents/update_status.html",context)



# admin leads 
@staff_member_required
def admin_leads(request):
    leads = Lead.objects.select_related("assigned_agent")

    context = {
        "page_title": "All Leads",
        "leads": leads,
    }

    return render(request,"admin/admin_leads.html", context)





# submit the lead 
def submit_lead(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        agents = User.objects.filter(is_staff=False, is_active=True)

        agent = min(
            agents,
            key=lambda a: Lead.objects.filter(assigned_agent=a).count(),
            default=None
        )

        Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
            assigned_agent=agent,
            assigned_at=now()
        )

        return redirect("lead_success")

    return render(
        request,
        "public/submit_lead.html",
        {"page_title": "Submit Lead"}
    )


# lead sucess message
def lead_success(request):
    return render(request,"public/sucess.html",{"page_title": "Success"})
