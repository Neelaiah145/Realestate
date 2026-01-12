from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def agent_leads(request):
        context = {
  
        "page_title": "Leads",
    }
        return render(request,'agents/agents_leads.html',context)



@login_required
def admin_leads(request):
    context = {
        "is_admin": request.user.is_superuser, 
        "page_title": "Leads",
    }
    return render(request, "admin/admin_leads.html",context)