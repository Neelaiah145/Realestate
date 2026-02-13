import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import io, base64
from django.db.models.functions import TruncMonth
from django.db.models import Count
from apps.leads.models import Lead


def monthly_analytics():
    rows = list(
        Lead.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    if len(rows) == 0:
        return None

    df = pd.DataFrame(rows)
    df["month_label"] = df["month"].dt.strftime("%b %Y") #store the month and year in df["month_label"]--> this is variable type but it store the df type maan table wise
    
    labels = df["month_label"].tolist()
    sizes = df["total"].tolist()

    total_leads = sum(sizes)

    def show_counts(pct):
        count = int(round(pct * total_leads / 100.0))
        return f"{count}"

    plt.figure(figsize=(8,5))
    plt.pie(
        sizes,
        labels=labels,
        autopct=show_counts,   #using count
        startangle=90
    )
    # plt.bar(labels,sizes)
    # plt.xlabel('month')
    # plt.ylabel('total leads')
    # plt.title("Monthly Leads Count")
    plt.axis("equal")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()

    return image







# status of the leads 
def lead_status_analytics():
    rows = list(
        Lead.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    if len(rows) == 0:
        return None

    df = pd.DataFrame(rows)

    # Convert status to table format
    df["status_label"] = df["status"].str.title()

    labels = df["status_label"].tolist()
    sizes = df["total"].tolist()
    total_leads = sum(sizes)
    
    def show_counts(pct):
        count = int(round(pct * total_leads / 100.0))
        return f"{count}"

    plt.figure(figsize=(8, 5))
    plt.pie(
        sizes,
        labels=labels,
        autopct=show_counts,   #using count
        startangle=90
    )

    plt.axis("equal")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()

    return image



# agent wise leads 