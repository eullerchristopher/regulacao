from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.templatetags.static import static
from os.path import abspath

from .models import PacienteCirurgia, PacienteEspecialidade, PacienteExame, Agenda, AgendaUBS, AgendamentoPaciente, UBS_CHOICES, ESPECIALIDADE_CHOICES
from .forms import PacienteCirurgiaForm, PacienteEspecialidadeForm, PacienteExameForm

# ---------------------- REDIRECIONAMENTO POR GRUPO ----------------------
@login_required
def redirect_user(request):
    """
    Redireciona o usuário para a página certa conforme o grupo.
    """
    if request.user.groups.filter(name__iexact='regulador').exists():
        return redirect('regulacao')
    elif request.user.groups.filter(name__iexact='ubs').exists():
        return redirect('ubs')
    else:
        return redirect('login')

# ---------------------- CADASTRO DE USUÁRIO ----------------------
def cadastro(request):
    """
    Cria um novo usuário e adiciona automaticamente a um grupo.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        grupo_nome = request.POST.get("grupo")  # "regulador" ou "ubs"

        # Validação de senha
        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return redirect("cadastro")

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe.")
            return redirect("cadastro")

        # Cria o usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Cria o grupo se não existir e adiciona o usuário
        if grupo_nome:
            grupo, created = Group.objects.get_or_create(name=grupo_nome)
            user.groups.add(grupo)

        user.save()

        messages.success(request, f"Usuário criado com sucesso e adicionado ao grupo '{grupo_nome}'!")
        return redirect("login")

    # GET
    return render(request, "cadastro.html")

# ---------------------- TELAS PRINCIPAIS ----------------------
@login_required
def regulacao(request):
    return render(request, "regulacao.html")

@login_required
def ubs(request):
    return render(request, "ubs.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

# ---------------------- DASHBOARD ----------------------
@login_required
def dashboard(request):
    # ---------------------- LISTAS COMPLETAS (para totais) ----------------------
    exames_completos = PacienteExame.objects.all()
    especialidades_completos = PacienteEspecialidade.objects.all()
    cirurgias_completos = PacienteCirurgia.objects.all()

    total_exames = exames_completos.count()
    total_especialidades = especialidades_completos.count()
    total_cirurgias = cirurgias_completos.count()
    total_pacientes = total_exames + total_especialidades + total_cirurgias

    # ---------------------- LISTAS PARA EXIBIÇÃO ----------------------
    exames_lista = exames_completos.order_by('-hora_cadastro')
    especialidades_lista = especialidades_completos.order_by('-hora_cadastro')
    cirurgias_lista = cirurgias_completos.order_by('-hora_cadastro')

    # ---------------------- BUSCA ----------------------
    busca_exame = request.GET.get('busca_exame')
    busca_esp = request.GET.get('busca_esp')
    busca_cir = request.GET.get('busca_cir')

    if busca_exame:
        exames_lista = exames_lista.filter(
            Q(nome__icontains=busca_exame) |
            Q(sus__icontains=busca_exame) |
            Q(protocolo__icontains=busca_exame)
        )
    if busca_esp:
        especialidades_lista = especialidades_lista.filter(
            Q(nome__icontains=busca_esp) |
            Q(sus__icontains=busca_esp) |
            Q(protocolo__icontains=busca_esp)
        )
    if busca_cir:
        cirurgias_lista = cirurgias_lista.filter(
            Q(nome__icontains=busca_cir) |
            Q(sus__icontains=busca_cir) |
            Q(protocolo__icontains=busca_cir)
        )

    # ---------------------- PAGINAÇÃO ----------------------

    paginator_exames = Paginator(exames_lista, 10)
    page_exames = request.GET.get('page_exames')
    exames = paginator_exames.get_page(page_exames)

    paginator_esp = Paginator(especialidades_lista, 10)
    page_esp = request.GET.get('page_esp')
    especialidades = paginator_esp.get_page(page_esp)

    paginator_cir = Paginator(cirurgias_lista, 10)
    page_cir = request.GET.get('page_cir')
    cirurgias = paginator_cir.get_page(page_cir)

    # ---------------------- USUÁRIOS ----------------------
    reguladores = User.objects.filter(groups__name__iexact='regulador')
    usuarios_ubs = User.objects.filter(groups__name__iexact='ubs')
    total_reguladores = reguladores.count()
    total_ubs = usuarios_ubs.count()

    # ---------------------- AGENDAS ----------------------
    agendas = Agenda.objects.all().order_by('-criado_em')
    for agenda in agendas:
        agenda.verificar_status()

    context = {
        'exames': exames,
        'especialidades': especialidades,
        'cirurgias': cirurgias,
        'total_exames': total_exames,
        'total_especialidades': total_especialidades,
        'total_cirurgias': total_cirurgias,
        'total_pacientes': total_pacientes,
        'reguladores': reguladores,
        'usuarios_ubs': usuarios_ubs,
        'total_reguladores': total_reguladores,
        'total_ubs': total_ubs,
        'agendas': agendas,
        'busca_exame': busca_exame,
        'busca_esp': busca_esp,
        'busca_cir': busca_cir,
    }

    return render(request, 'dashboard.html', context)

# REMOVER USUARIO

@login_required
def remover_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    # impede deletar o próprio usuário
    if usuario == request.user:
        messages.error(request, "Você não pode remover seu próprio usuário.")
        return redirect('dashboard')

    usuario.delete()
    messages.success(request, "Usuário removido com sucesso.")

    return redirect('dashboard')

# LISTAR TODOS OS REGISTROS

@login_required
def listar_cirurgia(request):
    pacientes = PacienteCirurgia.objects.all()
    return render(request, "listar_cirurgia.html", {"pacientes": pacientes})

@login_required
def listar_especialidade(request):
    pacientes = PacienteEspecialidade.objects.all()
    return render(request, "listar_especialidade.html", {"pacientes": pacientes})

@login_required
def listar_exame(request):
    pacientes = PacienteExame.objects.all()
    return render(request, "listar_exame.html", {"pacientes": pacientes})

# ---------------------- CRUD CIRURGIA ----------------------
@login_required
def cadastrar_cirurgia(request):
    form = PacienteCirurgiaForm(request.POST or None)
    if form.is_valid():
        paciente = form.save(commit=False)
        paciente.criado_por = request.user
        paciente.save()
        return redirect("listar_cirurgia")
    return render(request, "cadastro_cirurgia.html", {"form": form})

@login_required
def listar_cirurgia(request):
    busca = request.GET.get('busca')

    pacientes_lista = PacienteCirurgia.objects.all().order_by('-hora_cadastro')

    if busca:
        pacientes_lista = pacientes_lista.filter(
            Q(nome__icontains=busca) |
            Q(sus__icontains=busca) |
            Q(protocolo__icontains=busca)
        )

    paginator = Paginator(pacientes_lista, 10)
    page = request.GET.get('page')
    pacientes = paginator.get_page(page)

    return render(request, "listar_cirurgia.html", {
        "pacientes": pacientes,
        "busca": busca, 
    })

@login_required
def editar_cirurgia(request, id):
    # Só permite editar o registro que o usuário criou
    paciente = get_object_or_404(PacienteCirurgia, id=id, criado_por=request.user)
    form = PacienteCirurgiaForm(request.POST or None, instance=paciente)
    if form.is_valid():
        form.save()
        return redirect("listar_cirurgia")
    return render(request, "cadastro_cirurgia.html", {"form": form})

@login_required
def remover_cirurgia(request, id):
    paciente = get_object_or_404(PacienteCirurgia, id=id)  # sem filtro por usuário
    paciente.delete()
    return redirect("listar_cirurgia")

# ---------------------- CRUD ESPECIALIDADE ----------------------
@login_required
def cadastrar_especialidade(request):
    form = PacienteEspecialidadeForm(request.POST or None)
    if form.is_valid():
        paciente = form.save(commit=False)
        paciente.criado_por = request.user
        paciente.save()
        return redirect("listar_especialidade")
    return render(request, "cadastro_especialidade.html", {"form": form})

@login_required
def listar_especialidade(request):
    busca = request.GET.get('busca')

    pacientes_lista = PacienteEspecialidade.objects.all().order_by('-hora_cadastro')

    if busca:
        pacientes_lista = pacientes_lista.filter(
            Q(nome__icontains=busca) |
            Q(sus__icontains=busca)
        )

    paginator = Paginator(pacientes_lista, 10)

    page = request.GET.get('page')
    pacientes = paginator.get_page(page)

    return render(request, "listar_especialidade.html", {
        "pacientes": pacientes,
        "busca": busca
    })

@login_required
def editar_especialidade(request, id):
    paciente = get_object_or_404(PacienteEspecialidade, id=id, criado_por=request.user)
    form = PacienteEspecialidadeForm(request.POST or None, instance=paciente)
    if form.is_valid():
        form.save()
        return redirect("listar_especialidade")
    return render(request, "cadastro_especialidade.html", {"form": form})

@login_required
def remover_especialidade(request, id):
    paciente = get_object_or_404(PacienteEspecialidade, id=id)
    paciente.delete()
    return redirect("listar_especialidade")


# ---------------------- CRUD EXAME ----------------------

@login_required
def cadastrar_exame(request):
    form = PacienteExameForm(request.POST or None)
    if form.is_valid():
        paciente = form.save(commit=False)
        paciente.criado_por = request.user
        paciente.save()
        return redirect("listar_exame")
    return render(request, "cadastro_exame.html", {"form": form})

@login_required
def listar_exame(request):
    busca = request.GET.get('busca')

    pacientes_lista = PacienteExame.objects.all().order_by('-hora_cadastro')

    if busca:
        pacientes_lista = pacientes_lista.filter(
            Q(nome__icontains=busca) |
            Q(sus__icontains=busca)
        )

    paginator = Paginator(pacientes_lista, 10)

    page = request.GET.get('page')
    pacientes = paginator.get_page(page)

    return render(request, "listar_exame.html", {
        "pacientes": pacientes,
        "busca": busca
    })

@login_required
def editar_exame(request, id):
    paciente = get_object_or_404(PacienteExame, id=id, criado_por=request.user)
    form = PacienteExameForm(request.POST or None, instance=paciente)
    if form.is_valid():
        form.save()
        return redirect("listar_exame")
    return render(request, "cadastro_exame.html", {"form": form})

@login_required
def remover_exame(request, id):
    paciente = get_object_or_404(PacienteExame, id=id)
    paciente.delete()
    return redirect("listar_exame")

# ---------------------- COMPROVANTE ----------------------

# COMPROVANTE CIRURGIA

@login_required
def comprovante_cirurgia(request, id):
    paciente = get_object_or_404(PacienteCirurgia, id=id)

    template = get_template("comprovante_cirurgia.html")

    logo_path = abspath(static('assets/img/logo_img.jpeg'))

    context = {
        "paciente": paciente,
        "logo_path": logo_path
    }

    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'filename="comprovante_{paciente.nome}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

# COMPROVANTE ESPECIALIDADE

@login_required
def comprovante_especialidade(request, id):
    paciente = get_object_or_404(PacienteEspecialidade, id=id)

    template = get_template("comprovante_especialidade.html")

    logo_path = abspath(static('assets/img/logo_img.jpeg'))

    context = {
        "paciente": paciente,
        "logo_path": logo_path
    }

    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'filename="comprovante_{paciente.nome}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

# COMPROVANTE EXAME

@login_required
def comprovante_exame(request, id):
    paciente = get_object_or_404(PacienteExame, id=id)

    template = get_template("comprovante_exame.html")

    logo_path = abspath(static('assets/img/logo_img.jpeg'))

    context = {
        "paciente": paciente,
        "logo_path": logo_path
    }

    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'filename="comprovante_{paciente.nome}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

# PACIENTES AGENDADOS

@login_required
def pdf_pacientes_agendados(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    pacientes = agenda.agendamentopaciente_set.all()

    template = get_template("pdf_pacientes_agendados.html")

    logo_path = abspath(static('assets/img/logo_img.jpeg'))

    context = {
        "agenda": agenda,
        "pacientes": pacientes,
        "logo_path": logo_path
    }

    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'filename="agenda_{agenda_id}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response
# ---------------------- AGENDA ----------------------

# CRIAR AGENDA

@login_required
def criar_agenda(request):
    if request.method == "POST":
        especialidade = request.POST['especialidade']
        data = request.POST['data']
        total_vagas = int(request.POST['total_vagas'])
        vagas_por_ubs = int(request.POST['vagas_por_ubs'])

        total_ubs = len(UBS_CHOICES)
        vagas_regulacao = total_vagas - (vagas_por_ubs * total_ubs)

        agenda = Agenda.objects.create(
            especialidade=especialidade,
            data=data,
            total_vagas=total_vagas,
            vagas_por_ubs=vagas_por_ubs,
            vagas_regulacao=vagas_regulacao,
            criado_por=request.user
        )

        for ubs in UBS_CHOICES:
            AgendaUBS.objects.create(
                agenda=agenda,
                ubs=ubs[0],
                vagas=vagas_por_ubs
            )

        return redirect('dashboard')

    return render(request, "criar_agenda.html", {"especialidades": ESPECIALIDADE_CHOICES})

# VER ESPECIALIDADE

@login_required
def agendas_especialidade(request, especialidade):
    agendas = Agenda.objects.filter(especialidade=especialidade)
    return render(request,"agenda_especialidade.html",{
        "agendas":agendas,
        "especialidade":especialidade
    })

# AGENDAR PACIENTE

@login_required
def agendar_paciente(request, id):
    agenda = get_object_or_404(Agenda, id=id)
    if request.method == "POST":
        ubs_selecionada = request.POST['ubs']

        # Verifica vagas restantes
        agenda_ubs = AgendaUBS.objects.get(agenda=agenda, ubs=ubs_selecionada)
        if agenda_ubs.vagas_restantes() <= 0:
            messages.error(request, "Não há vagas disponíveis nesta UBS.")
            return redirect('agenda_especialidade', especialidade=agenda.especialidade)

        # Criar agendamento
        AgendamentoPaciente.objects.create(
            agenda=agenda,
            nome=request.POST['nome'],
            sus=request.POST['sus'],
            telefone=request.POST['telefone'],
            agente=request.POST['agente'],
            ubs=ubs_selecionada,
            criado_por=request.user
        )

        # Atualiza vagas usadas
        agenda_ubs.vagas_usadas += 1
        agenda_ubs.save()

        # Mensagem de sucesso
        messages.success(request, f"Paciente {request.POST['nome']} agendado com sucesso!")

        # Redireciona para o dashboard/menu
        return redirect('ubs')  # <- aqui vai para o menu

    return render(request,"agendar_paciente.html",{"agenda":agenda,"ubs":UBS_CHOICES})

# REMOVER PACIENTE DA AGENDA

@login_required
def remover_paciente_agenda(request, paciente_id):
    paciente = get_object_or_404(AgendamentoPaciente, id=paciente_id)
    agenda = paciente.agenda
    ubs = paciente.ubs

    # Recupera a UBS da agenda e devolve a vaga
    agenda_ubs = AgendaUBS.objects.get(agenda=agenda, ubs=ubs)
    if agenda_ubs.vagas_usadas > 0:
        agenda_ubs.vagas_usadas -= 1
        agenda_ubs.save()

    paciente.delete()
    messages.success(request, f"Paciente {paciente.nome} removido e vaga devolvida para {ubs}.")
    return redirect('dashboard')

# APAGAR AGENDA

@login_required
def remover_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)

    # Deletar pacientes e vagas automaticamente
    AgendamentoPaciente.objects.filter(agenda=agenda).delete()
    AgendaUBS.objects.filter(agenda=agenda).delete()
    agenda.delete()

    messages.success(request, "Agenda removida com sucesso.")
    return redirect('dashboard')

