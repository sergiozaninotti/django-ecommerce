from django.template import RequestContext
from categorias.models import Category
from tema import models

def app(request):
    return {'app': {
        'tema': models.Logo,
        'categorias': Category.objects.all().values_list('categoria', flat=True)
    }}