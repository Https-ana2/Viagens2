from django.shortcuts import render, get_object_or_404, redirect
from .models import Pacote
from .forms import ContatoForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal

# 1. PÁGINA INICIAL (Com busca)

def index(request):
    lista_pacotes = Pacote.objects.filter(ativo=True)
    
    if 'buscando' in request.GET:
        nome_a_buscar = request.GET['buscando']
        if nome_a_buscar:
            lista_pacotes = lista_pacotes.filter(nome__icontains=nome_a_buscar)

    # destacar apenas pacotes que têm imagem (evita slides com placeholder)
    destaque = lista_pacotes.exclude(imagem='')[:5]

    return render(request, 'viagens/index.html', {'pacotes': lista_pacotes, 'destaque': destaque})

def detalhes(request, pacote_id):
    pacote = get_object_or_404(Pacote, pk=pacote_id)
    
    return render(request, 'viagens/detalhes.html', {'pacote': pacote})

# 3. CADASTRO DE USUÁRIO

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/cadastro.html', {'form': form})

# 4. ADICIONAR AO CARRINHO (Lógica da Sessão)

def adicionar_carrinho(request, pacote_id):
    # garante que a sessão tem lista de ids
    if 'carrinho' not in request.session:
        request.session['carrinho'] = []

    carrinho = request.session['carrinho']

    # armazenar ids como inteiros (coerção segura)
    try:
        pid = int(pacote_id)
    except (TypeError, ValueError):
        return redirect('index')

    if pid not in [int(x) for x in carrinho]:
        carrinho.append(pid)

    request.session['carrinho'] = carrinho

    return redirect('index')

# 5. VER O CARRINHO 

def ver_carrinho(request):
    # obtém ids da sessão e garante inteiros válidos
    raw_ids = request.session.get('carrinho', [])
    ids_carrinho = []
    for i in raw_ids:
        try:
            ids_carrinho.append(int(i))
        except (TypeError, ValueError):
            continue

    pacotes_no_carrinho = Pacote.objects.filter(id__in=ids_carrinho)

    total = sum((p.preco for p in pacotes_no_carrinho), Decimal('0'))

    return render(request, 'viagens/carrinho.html', {'pacotes': pacotes_no_carrinho, 'total': total})


def remover_carrinho(request, pacote_id):
    # remove um pacote do carrinho (se presente)
    if 'carrinho' not in request.session:
        return redirect('ver_carrinho')

    try:
        pid = int(pacote_id)
    except (TypeError, ValueError):
        return redirect('ver_carrinho')

    carrinho = request.session.get('carrinho', [])
    # normaliza para ints
    carrinho_ints = [int(x) for x in carrinho if str(x).isdigit()]
    if pid in carrinho_ints:
        carrinho_ints.remove(pid)
    request.session['carrinho'] = carrinho_ints
    return redirect('ver_carrinho')


def contato(request):
    """Exibe o formulário de contato e salva a mensagem no banco."""
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua mensagem foi enviada. Entraremos em contato em breve!')
            return redirect('contato')
    else:
        form = ContatoForm()

    return render(request, 'viagens/contato.html', {'form': form})