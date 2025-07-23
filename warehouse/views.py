from django.shortcuts import render


# Create your views here.
def show_index(request):
    return render(request, "index.html")


def show_personal_account(request):
    return render(request, "my-rent.html")


def show_faq(request):
    return render(request, "faq.html")


def show_boxes(request):
    return render(request, "boxes.html")
