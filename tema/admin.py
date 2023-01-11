from django.contrib import admin
from . import models

class LogoInline(admin.ModelAdmin):
    model = models.Logo

class TemaAdmin(admin.ModelAdmin):
    list_display = ['nome_do_layout', 'slider_1', 'slider_2', 'slider_3']

admin.site.register(models.Tema, TemaAdmin)
admin.site.register(models.Logo)