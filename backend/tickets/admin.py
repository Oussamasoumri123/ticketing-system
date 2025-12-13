from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'description', 'status')
        }),
        ('Utilisateur', {
            'fields': ('created_by',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')