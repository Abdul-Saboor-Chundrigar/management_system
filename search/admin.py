from django.contrib import admin
from .models import SearchLog

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'field', 'timestamp', 'user')
    list_filter = ('field', 'timestamp')
    search_fields = ('query', 'field')
