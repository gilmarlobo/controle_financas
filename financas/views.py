from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models import Sum
from .forms import GastoForm
from .models import Gasto
from django.core.paginator import Paginator


def index(request):
    hoje = now().date()

    # Calcular total gasto no mês
    gasto_total = Gasto.objects.filter(
        data__year=hoje.year, data__month=hoje.month).aggregate(Sum('valor'))['valor__sum'] or 0
    gasto_total_formatado = f"R$ {gasto_total:,.2f}".replace(
        ",", "X").replace(".", ",").replace("X", ".")

    # Pegar valores dos filtros
    filtro_mes = request.GET.get('mes', '')
    filtro_data = request.GET.get('data', '')
    filtro_descricao = request.GET.get('descricao', '')

    # Inicializar a queryset de gastos
    if filtro_mes:
        ano, mes = map(int, filtro_mes.split('-'))
        gastos = Gasto.objects.filter(data__year=ano, data__month=mes)
    else:
        gastos = Gasto.objects.filter(data__year=hoje.year, data__month=hoje.month)

    # Aplicar filtros adicionais
    if filtro_data:
        gastos = gastos.filter(data=filtro_data)
    if filtro_descricao:
        gastos = gastos.filter(descricao__icontains=filtro_descricao)

    # Ordenar os gastos (os mais recentes primeiro)
    gastos = gastos.order_by('-data', '-id')

    # Verificar se algum filtro foi aplicado
    filtros_aplicados = filtro_mes or filtro_data or filtro_descricao

    if filtros_aplicados:
        # Se filtros foram aplicados, não usar paginação
        gastos_paginados = gastos
    else:
        # Se nenhum filtro foi aplicado, usar paginação
        lista = gastos
        paginator = Paginator(lista, 10)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = paginator.num_pages
        gastos_paginados = paginator.get_page(page_number)

    # Calcular a soma dos valores filtrados
    gasto_filtrado_total = gastos.aggregate(Sum('valor'))['valor__sum'] or 0
    gasto_filtrado_total_formatado = f"R$ {gasto_filtrado_total:,.2f}".replace(
        ",", "X").replace(".", ",").replace("X", ".")

    return render(request, 'financas/index.html', {
        'gasto_total': gasto_total_formatado,
        'gastos': gastos_paginados,
        'gasto_filtrado_total': gasto_filtrado_total_formatado,
        'filtro_mes': filtro_mes,
        'filtro_data': filtro_data,
        'filtro_descricao': filtro_descricao,
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


def lista(request):
    gasto = Gasto.objects.all()

    return render(request, 'financas/lista.html', {'gasto': gasto})
