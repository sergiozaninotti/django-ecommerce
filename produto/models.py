from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from helpers import helpers
from categorias.models import Category

class Produto(models.Model):

    nome = models.CharField(max_length=150)
    categoria = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    descricao_longa = models.TextField(max_length=255)
    descricao_curta = models.TextField()
    imagem = models.ImageField(upload_to='product_images/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Preço Promo')
    tipo = models.CharField(  #cria um select no admin
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return helpers.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return helpers.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo'

    #salva a imagem no admin
    def save(self, *args, **kwargs):

        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        #se existir uma imagem, manda a imagem do model e o tamanho pro metodo statico
        if self.imagem:
            helpers.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    #no admin mostra o nome da class, esta class altera o nome de exibição
    class Meta:
        verbose_name = 'Variavel'
        verbose_name_plural = 'Variaveis'