from django.contrib import admin
from . import models

class CategoryAdmin(admin.ModelAdmin):

    list_display = ['categoria']

admin.site.register(models.Category, CategoryAdmin)
