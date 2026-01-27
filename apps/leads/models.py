from django.db import models
from django.conf import settings


class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
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
    # BASIC LEAD INFO
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)

    # AGENT ASSIGNMENT
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,    
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads"
    )
    
    # new column for associates
    assigned_associate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associate_leads",
        limit_choices_to={"role": "associate"}
    )
    # CRM STATUS (CONTROLLED)
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

    # ======================
    # CALL FEEDBACK
    # ======================
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
    
    
    # AGENT MANUAL RESPONSE (FREE TEXT)
    
    agent_note = models.TextField(
        blank=True,
        help_text="Agent call response / remarks"
    )

    # FOLLOW-UP REMINDER
    follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Next follow-up date & time"
    )

    # TIMESTAMPS
    assigned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_update_lead","can update lead"),
            ("can_delete_lead","can delete lead"),
            ("can_book_lead","can book lead"),
        ]