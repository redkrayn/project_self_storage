from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from reviews.models import Review
from custom_user.forms import LoginForm, RegistrationForm


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


@login_required
def show_profile(request):
    return render(request, "profile.html")