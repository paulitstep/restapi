from django.contrib import admin

from .models import Update


class UpdateAdmin(admin.ModelAdmin):
    list_display = ('content', 'timestamp', 'updated')


admin.site.register(Update, UpdateAdmin)
