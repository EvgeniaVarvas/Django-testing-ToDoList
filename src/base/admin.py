from django.contrib import admin

from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','created', 'complete')
    list_filter = ('complete',)
    search_fields = ('title', 'description')