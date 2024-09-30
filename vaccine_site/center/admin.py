from django.contrib import admin
from center.models import Center, Storage


class StorageInline(admin.TabularInline):
    model = Storage
    readonly_fields = ["booked_quantity"]
    
class CustomCenterAdmin(admin.ModelAdmin):
    inlines = [StorageInline]
    search_fields = ["name", "address"]
    list_display = ["name", "address"]

admin.site.register(Center, CustomCenterAdmin)
# admin.site.register(Storage)