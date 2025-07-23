from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'slogan', 'created_at')
    search_fields = ('full_name', 'city', 'slogan')
    list_filter = ('city',)
