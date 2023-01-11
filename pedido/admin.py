from django.contrib import admin
from . import models

#registra na mesma tela do pedido o ItemPedido no admin
class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]

admin.site.register(models.Pedido)
admin.site.register(models.ItemPedido)
