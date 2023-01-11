from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from helpers import helpers
from .models import Pedido, ItemPedido


class DispatchLoginRequeriredMixin(View):
    # Método que verifica se o usuário esta logado se ele tentar acessar algum pedido pela url
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    # mostra apenas as informações do usuário logado
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # filtra a consulta pelo usuario logado
        qs = qs.filter(usuario=self.request.user)
        return qs

# O sistema sempre irá buscar a primeira classe para depois executar a proxima


class Pagar(DispatchLoginRequeriredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'  # parametro vindo da url
    context_object_name = 'pedido'


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Faça seu login para continuar!'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio :('
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [id for id in carrinho]
        db_variacoes = list(
            # se puxar mais de 1 tabela, usar o select_related pois faz inner join e transforma e menos consultas
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        for variacao in db_variacoes:

            # chave tem que ser string pois esta sendo usada no json
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promo']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promo'] = estoque * \
                    preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho :( <br>' \
                                    'Reduzimos a quantidade, verique novamente seu carrinho.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = helpers.cart_total_items(carrinho)
        valor_total_carrinho = helpers.cart_total_value(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        pedido.save()

        # bulk_create cria uma queryset com varios objetos, insere no db varios objetos de uma unica vez
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promo'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        context = {
            'qtd_total_carrinho': qtd_total_carrinho,
            'valor_total_carrinho': valor_total_carrinho
        }

        del self.request.session['carrinho']
        # usado o reserve para passar o id do produto via url
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )
        # renderiza = render(self.request, self.template_name, context)


class Detalhe(DispatchLoginRequeriredMixin, DetailView):
    template_name = 'pedido/detalhe.html'
    model = Pedido
    context_object_name = 'pedido'
    pk_url_kwarg = 'pk'


class ListarPedidos(DispatchLoginRequeriredMixin, ListView):
    template_name = 'pedido/listarpedidos.html'
    model = Pedido
    context_object_name = 'pedidos'
    paginate_by = 4
    ordering = ['-id']
