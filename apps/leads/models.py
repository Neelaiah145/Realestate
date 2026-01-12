from django.db import models
from django.conf import settings


class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("closed", "Closed"),
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

    # CRM STATUS (CONTROLLED)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

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

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
