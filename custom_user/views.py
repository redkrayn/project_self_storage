from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, RegistrationForm


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'redirect': '/profile/'})
            else:
                return JsonResponse({'error': 'Неправильный логин или пароль.'}, status=401)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': f'Некорректные данные формы {errors}'}, status=400)
    else:
        return redirect('/')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return JsonResponse({'message': 'Регистрация прошла успешно!'})
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    else:
        return redirect('/')
