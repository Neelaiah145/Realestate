from django.db import models
from django.conf import settings
from django.utils import timezone

class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("intersted", "Intersted"),
        ("closed", "Closed"),
    ]
    INTEREST_LEVEL_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    
    PURCHASE_TIMELINE_CHOICES = [
        ("immediate", "Immediate"),
        ("1-3", "1–3 Months"),
        ("3-6", "3–6 Months"),
        ("enquiry", "Just Enquiry"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ("plot", "Plot"),
        ("flat", "Flat"),
        ("villa", "Villa"),
        ("commercial", "Commercial"),
    ]
    # lead information
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)

    
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,    
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads"
    )
    
 
    assigned_associate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associate_leads",
        limit_choices_to={"role": "associate"}
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        blank=True
    )

    preferred_location = models.CharField(
        max_length=100,
        blank=True
    )

    budget_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    budget_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    purchase_timeline = models.CharField(
        max_length=20,
        choices=PURCHASE_TIMELINE_CHOICES,
        blank=True
    )

    # CALL FEEDBACK
   
    interest_level = models.CharField(
        max_length=10,
        choices=INTEREST_LEVEL_CHOICES,
        blank=True
    )

    next_action = models.CharField(
        max_length=255,
        blank=True
    )

    client_response = models.TextField(blank=True)
    objections = models.TextField(blank=True)
    
    
 
    
    agent_note = models.TextField(
        blank=True,
        help_text="Agent call response / remarks"
    )

  
    follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Next follow-up date & time"
    )

    
    assigned_at = models.DateTimeField(null=True, blank=True)   
    created_at  = models.DateTimeField(auto_now_add=True)       
    updated_at  = models.DateTimeField(auto_now=True)   
    class Meta:
        permissions = [
            ("view_leads","View Leads Page(Menu)"),
            ("can_update_lead","can update lead"),
            ("can_delete_lead","can delete lead"),
            ("can_book_lead","can book lead"),
            ("view_contacts","View Contacts"),
            ("change_contact","Change_Contact"),
            ("delete_contact","Delete_Contact"),
            
        ]


class LeadHistory(models.Model):
 
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="histories"
    )
    
    # Core fields to track - mirrors Lead model fields
    status = models.CharField(
        max_length=20,
        choices=Lead.STATUS_CHOICES
    )
    
    property_type = models.CharField(
        max_length=20,
        choices=Lead.PROPERTY_TYPE_CHOICES,
        blank=True
    )
    
    preferred_location = models.CharField(
        max_length=100,
        blank=True
    )
    
    budget_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    budget_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    purchase_timeline = models.CharField(
        max_length=20,
        choices=Lead.PURCHASE_TIMELINE_CHOICES,
        blank=True
    )
    
    # Call feedback fields
    interest_level = models.CharField(
        max_length=10,
        choices=Lead.INTEREST_LEVEL_CHOICES,
        blank=True
    )
    
    next_action = models.CharField(
        max_length=255,
        blank=True
    )
    
    client_response = models.TextField(blank=True)
    objections = models.TextField(blank=True)
    agent_note = models.TextField(blank=True)
    
    # Follow-up tracking
    follow_up_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # Audit fields - WHO made the change and WHEN
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lead_updates"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]  # Most recent first
        verbose_name = "Lead History"
        verbose_name_plural = "Lead Histories"
        indexes = [
            models.Index(fields=['lead', '-created_at']),  # Optimize queries
        ]
    
    def __str__(self):
        return f"{self.lead.name} - {self.get_status_display()} - {self.created_at.strftime('%d %b %Y, %I:%M %p')}"
    
    def get_changes_summary(self):
        """Helper method to get a quick summary of what changed"""
        changes = []
        if self.status:
            changes.append(f"Status: {self.get_status_display()}")
        if self.agent_note:
            changes.append(f"Note added")
        if self.follow_up_at:
            changes.append(f"Follow-up scheduled")
        return ", ".join(changes) if changes else "Updated"