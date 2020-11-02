from django.contrib import admin
from .models import Profile

def make_aviable(modeladmin, request, queryset):
    queryset.update(avialble=True)
make_aviable.short_description = "Mark selected users as avialble"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avialble']
    ordering = ['user']
    actions = [make_aviable]
admin.site.register(Profile,ProfileAdmin)
