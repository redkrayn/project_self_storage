from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from custom_user.views import login_view, register
from warehouse import views
from warehouse.views import (
    show_boxes,
    show_faq,
    show_index,
    show_personal_account,
    show_profile,
)

urlpatterns = [
    path("calculate-cost/", views.calculate_cost, name="calculate_cost"),
    path("admin/", admin.site.urls),
    path("", show_index, name="index"),
    path("personal-account/", show_personal_account, name="personal-account"),
    path("faq/", show_faq, name="faq"),
    path("boxes/", show_boxes, name="boxes"),
    path("boxes/<int:warehouse_id>/", show_boxes, name="box"),
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("profile/", show_profile, name="profile"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
