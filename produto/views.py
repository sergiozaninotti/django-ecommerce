from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from tema.models import Tema
from categorias.models import Category
from perfil.models import Perfil
from django.contrib import messages
from django.db.models import Q  # Q é usado para buscas com filtros
from pprint import pprint  # formata um dicionario para melhor visualização

"""
Reverse pega o http referer anterior do visitante com get()
"""

class ListaProdutos(ListView):
    """
    context_object_name é a variavel que vai para o template
    """
    template_name = 'produto/lista.html'
    context_object_name = 'context'
    queryset = {
        'produto': models.Produto.objects.all(),
        'categoria': Category.objects.all().values_list(),
        'tema': Tema.objects.all().values_list().first(),
    }

class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )
        self.request.session.save()
        return qs

class DetalheProduto(DetailView):
    """def get(self, *args, **kwargs):
        return HttpResponse('DetalheProduto')"""
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe!'
            )
            return redirect(http_referer)

        # tenta pegar o id da variacao do DB se não existir manda um 404
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        variacao_estoque = variacao.estoque
        produto = variacao.produto  # pega a class variacao e class produto do model

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promo = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.warning(
                self.request,
                'Desculpe! Estamos sem estoque deste produto :('
            )
            redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        # verifica se a variacao existe no carrinho
        if variacao_id in carrinho:
            # sempre que vir neste if, o usuário esta tentando adicionar uma nova variacao no carrinho
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Desculpe! Estamos sem {quantidade_carrinho} unidades de {produto_nome} em estoque! '
                    f'Adicionamos {variacao_estoque} no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promo'] = preco_unitario_promo * quantidade_carrinho

        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promo': preco_unitario_promo,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promo': preco_unitario_promo,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(
            self.request,
            'Produto adicionado ao carrinho!'
        )
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho']

        messages.success(
            self.request,
            f'Produto removido do carrinho!'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        context = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(self.request, 'produto/carrinho.html', context)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):

        perfil = Perfil.objects.filter(usuario=self.request.user).first()

        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil!'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio!'
            )
            return redirect('produto:lista')

        context = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
            'perfil': perfil
        }
        return render(self.request, 'produto/resumodacompra.html', context)
