from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Успешный вход!'})
            else:
                return JsonResponse({'error': 'Неправильный логин или пароль.'}, status=401)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': f'Некорректные данные формы {errors}'}, status=400)
    else:
        return redirect('/')
