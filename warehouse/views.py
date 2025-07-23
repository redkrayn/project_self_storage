from django.shortcuts import render
from reviews.models import Review
from custom_user.forms import LoginForm

# Create your views here.
def show_index(request):
    if request.method == "GET":
        form = LoginForm()
        reviews = Review.objects.all()
        return render(request, "index.html", {"reviews": reviews, "form": form})


def show_personal_account(request):
    return render(request, "my-rent.html")


def show_faq(request):
    return render(request, "faq.html")


def show_boxes(request):
    return render(request, "boxes.html")
