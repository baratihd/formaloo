from django.contrib import admin

from .models import App


__all__ = ('AppAdmin', 'verify_apps')


@admin.action(description='Mark selected apps as verified')
def verify_apps(modeladmin, request, queryset):  # noqa
    queryset.update(is_verified=True)


class AppAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'price', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    actions = [verify_apps]


admin.site.register(App, AppAdmin)
