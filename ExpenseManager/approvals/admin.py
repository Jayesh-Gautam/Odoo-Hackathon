from django.contrib import admin
from .models import ApprovalFlow, ApprovalStep, ApprovalRule, ApprovalLog

class ApprovalStepInline(admin.TabularInline):
    model = ApprovalStep
    extra = 1

@admin.register(ApprovalFlow)
class ApprovalFlowAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_default')
    inlines = [ApprovalStepInline]

admin.site.register(ApprovalRule)
admin.site.register(ApprovalLog)
