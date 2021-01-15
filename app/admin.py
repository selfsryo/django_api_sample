from django.contrib import admin

from app.models import Office, Combi


class OfficeAdmin(admin.ModelAdmin):
    pass


class CombiAdmin(admin.ModelAdmin):
    list_display = ('name', 'office')
    list_display_links = list_display


admin.site.register(Office, OfficeAdmin)
admin.site.register(Combi, CombiAdmin)
