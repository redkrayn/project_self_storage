from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from custom_user.forms import LoginForm, RegistrationForm
from reviews.models import Review

from .models import Cell, Request, Warehouse


def show_index(request):
    reviews = Review.objects.all()
    random_warehouse = Warehouse.objects.with_cell_counts().order_by("?").first()
    return render(
        request,
        "index.html",
        {
            "warehouse": random_warehouse,
            "form": LoginForm(),
            "registration_form": RegistrationForm(),
            "reviews": reviews,
            "user": request.user,
            "is_authenticated": request.user.is_authenticated,
        },
    )


def ajax_cells(request):
    warehouse_id = request.GET.get("warehouse_id")
    cells = Cell.objects.filter(warehouse_id=warehouse_id)
    rendered_template = render_to_string(
        "cells_box.html", {"cells": cells}
    )
    return JsonResponse({"template": rendered_template}, safe=False)


def show_personal_account(request):
    return render(request, "my-rent.html")


def show_faq(request):
    return render(request, "faq.html")


def show_boxes(request, warehouse_id=None):
    if not warehouse_id:
        warehouse_id = Warehouse.objects.order_by("name").first().id
    warehouses = Warehouse.objects.with_cell_counts().all()
    return render(
        request, "boxes.html", {"warehouses": warehouses, "warehouse_id": warehouse_id}
    )


def calculate_cost(request):
    if request.method == "POST":
        email = request.POST.get("EMAIL1") or request.POST.get("EMAIL2")
        if email:
            try:
                send_mail(
                    "Hi everynyan",
                    "здарова, солнце, еда",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                Request.objects.create(email=email)
            except Exception as e:
                print(f"Ошибка отправки: {e}")
        return redirect("index")
    return redirect("index")


@login_required
def show_profile(request):
    return render(request, "profile.html")
