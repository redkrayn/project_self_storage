from django.shortcuts import render
from reviews.models import Review


# Create your views here.
def show_index(request):
    reviews = Review.objects.all()
    return render(request, "index.html", {"reviews": reviews})


def show_personal_account(request):
    return render(request, "my-rent.html")


def show_faq(request):
    return render(request, "faq.html")


def show_boxes(request):
    return render(request, "boxes.html")
