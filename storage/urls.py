from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from custom_user.views import login_view, register
from warehouse.views import (
    show_boxes,
    show_faq,
    show_index,
    show_profile,
    ajax_cells,
    add_order,
    calculate_cost
)

urlpatterns = [
    path("calculate-cost/", calculate_cost, name="calculate_cost"),
    path("admin/", admin.site.urls),
    path("", show_index, name="index"),
    path("faq/", show_faq, name="faq"),
    path("boxes/", show_boxes, name="boxes"),
    path("boxes/<int:warehouse_id>/", show_boxes, name="box"),
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("profile/", show_profile, name="profile"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path("ajax_cells/", ajax_cells, name="ajax_cells"),
    path("add_order/<int:cell_id>/", add_order, name="add_order")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
