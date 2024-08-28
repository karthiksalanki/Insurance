from django.contrib import admin
from .models import Policy, Comment
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Policy)
class PolicyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('application_number', 'customer_name', 'email', 'policy_status', 'created_at')
    search_fields = ('application_number', 'email', 'customer_name', 'policy_status')
    list_filter = ('policy_status','customer_name', 'created_at')
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('policy__application_number', 'comment_text', 'created_at')
    search_fields = ('policy__application_number', 'comment_text')