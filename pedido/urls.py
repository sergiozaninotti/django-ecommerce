from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('listarpedidos/', views.ListarPedidos.as_view(), name='listarpedidos'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
]