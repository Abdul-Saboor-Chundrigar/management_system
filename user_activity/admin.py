from django.contrib import admin
from .models import UserActivity

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'url')
    list_filter = ('activity_type', 'user')
    search_fields = ('user__username', 'url')
    readonly_fields = ('details_preview',)

    def details_preview(self, obj):
        return format_html("<pre>{}</pre>", json.dumps(obj.details, indent=2))
    details_preview.short_description = "Activity Details"
