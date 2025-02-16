from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models import Sum
from .forms import GastoForm
from .models import Gasto
from django.core.paginator import Paginator


def index(request):
    hoje = now().date()

    # Calcular total gasto no mês
    gasto_total = Gasto.objects.filter(data__year=hoje.year, data__month=hoje.month).aggregate(Sum('valor'))['valor__sum'] or 0
    gasto_total_formatado = f"R$ {gasto_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Pegar valores dos filtros
    filtro_data = request.GET.get('data', '')
    filtro_descricao = request.GET.get('descricao', '')

    # Inicializar a queryset de gastos
    gastos = Gasto.objects.filter(data__year=hoje.year, data__month=hoje.month)

    # Aplicar filtros se existirem
    if filtro_data:
        gastos = gastos.filter(data=filtro_data)
    if filtro_descricao:
        gastos = gastos.filter(descricao__icontains=filtro_descricao)

    # Ordenar os gastos por data
    gastos = gastos.order_by('data')

    # Paginação - 10 itens por página
    paginator = Paginator(gastos, 10)
    page_number = request.GET.get('page')
    gastos_paginados = paginator.get_page(page_number)

    # Calcular a soma dos valores filtrados
    gasto_filtrado_total = gastos.aggregate(Sum('valor'))['valor__sum'] or 0
    gasto_filtrado_total_formatado = f"R$ {gasto_filtrado_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return render(request, 'financas/index.html', { 
        'gasto_total': gasto_total_formatado,
        'gastos': gastos_paginados,  # Agora está paginado
        'gasto_filtrado_total': gasto_filtrado_total_formatado,
        'filtro_data': filtro_data,
        'filtro_descricao': filtro_descricao
    })

def registrar_gasto(request):
    data = request.GET.get('data', None)  # Captura a data da URL

    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            if data:
                gasto.data = data  # Salva a data capturada da URL
            gasto.save()
            return redirect('index')  # Redireciona após salvar

    else:
        form = GastoForm()

    return render(request, 'financas/registrar_gasto.html', {'form': form, 'data': data})

