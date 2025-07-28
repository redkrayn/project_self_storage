from django.urls import path
from warehouse import views
"""
URL configuration for storage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from warehouse.views import show_index, show_personal_account, show_faq, show_boxes, show_profile
from custom_user.views import login_view, register
urlpatterns = [
    path('calculate-cost/', views.calculate_cost, name='calculate_cost'),
    path('admin/', admin.site.urls),
    path('', show_index, name='index'),
    path('personal-account/', show_personal_account, name='personal-account'),
    path('faq/', show_faq, name='faq'),
    path('boxes/', show_boxes, name='boxes'),
    path('boxes/<int:warehouse_id>/', show_boxes, name='box'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', show_profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
