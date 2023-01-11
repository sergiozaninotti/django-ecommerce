from django.contrib import admin
from . import models

# deixa uma nova linha em branco na variação para facilitar
class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1

# dentro do produto inlines, insere a linha da variação acima
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [
        VariacaoInline
    ]

admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)