from typing import List
from django.contrib import admin

from .models import NewsletterUser


@admin.register(NewsletterUser)
class NewsletterUserAdmin(admin.ModelAdmin):
    list_display: List[str] = ['email', 'joined']
    search_fields: List[str] = ['email']
    list_filter: List[str] = ['joined']
