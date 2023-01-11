from django.db import models
from helpers import helpers
from django.conf import settings
from categorias.models import Category
import os

class Logo(models.Model):

    def upload_callback(instance, filename):
        filename = 'logo.png'
        return os.path.join('theme/images', filename)

    logo = models.ImageField(upload_to=upload_callback, blank=True, null=True)

    def save(self, *args, **kwargs):
        # verifica se existe, se sim, deleta e coloca a nova
        if os.path.exists(settings.MEDIA_ROOT + '/theme/images/logo.png'):
            os.remove(settings.MEDIA_ROOT + '/theme/images/logo.png')

        super().save(*args, **kwargs)

        helpers.resize_image(self.logo, 300, None, 'png')

    def __str__(self):
        return self.logo.name

    class Meta:
        verbose_name = 'Logo'
        verbose_name_plural = 'Logo'

class Tema(models.Model):
    nome_do_layout = models.CharField(max_length=128)
    slider_1 = models.ForeignKey(Category, related_name='slider_1', default=1, null=False, on_delete=models.CASCADE)
    slider_2 = models.ForeignKey(Category, related_name='slider_2', default=1, null=False, on_delete=models.CASCADE)
    slider_3 = models.ForeignKey(Category, related_name='slider_3', default=1, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Personalização'
        verbose_name_plural = 'Personalizações'