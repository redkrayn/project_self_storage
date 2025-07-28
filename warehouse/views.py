from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from reviews.models import Review
from .models import Request
from custom_user.forms import LoginForm, RegistrationForm
from django.core.mail import send_mail, get_connection
from django.shortcuts import redirect
from django.conf import settings


def show_index(request):
    reviews = Review.objects.all()
    return render(request, 'index.html', {
        'form': LoginForm(),
        'registration_form': RegistrationForm(),
        'reviews': reviews,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    })


def show_personal_account(request):
    return render(request, "my-rent.html")


def show_faq(request):
    return render(request, "faq.html")


def show_boxes(request):
    return render(request, "boxes.html")


def calculate_cost(request):
    if request.method == 'POST':
        email = request.POST.get('EMAIL1') or request.POST.get('EMAIL2')
        if email:
            try:
                send_mail(
                    'Hi everynyan',
                    'здарова, солнце, еда',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                Request.objects.create(email=email)
            except Exception as e:
                print(f"Ошибка отправки: {e}")
        return redirect('index')
    return redirect('index')


@login_required
def show_profile(request):
    return render(request, "profile.html")


