"""Admin configuration for core app.

Customizes Django admin interface for:
- Contact message management
- Help category and article management
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, HelpCategory, HelpArticle

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'subject_display', 'status_badge', 'created_at')
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Reply', {
            'fields': ('reply', 'replied_at')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_display(self, obj):

        return obj.get_subject_display()
    subject_display.short_description = 'Subject'
    
    def status_badge(self, obj):

        status_colors = {
            'new': '#ffc107',
            'reading': '#17a2b8',
            'replied': '#28a745',
            'closed': '#6c757d',
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    ordering = ('-created_at',)

