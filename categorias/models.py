from django.db import models

class Category(models.Model):

    categoria = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

