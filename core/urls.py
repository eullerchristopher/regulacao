from django.urls import path
from . import views

urlpatterns = [
path('redirect/',views.redirect_user,name="redirect_user"),

path('cadastro/', views.cadastro, name='cadastro'),

#Paginas Principais
path('regulacao/',views.regulacao,name="regulacao"),
path('ubs/',views.ubs,name="ubs"),
path('dashboard/',views.dashboard,name="dashboard"),

# Cirurgia
path('cadastrar_cirurgia/', views.cadastrar_cirurgia, name="cadastrar_cirurgia"),
path('listar_cirurgia/', views.listar_cirurgia, name="listar_cirurgia"),
path('editar_cirurgia/<int:id>/', views.editar_cirurgia, name="editar_cirurgia"),
path('remover_cirurgia/<int:id>/', views.remover_cirurgia, name="remover_cirurgia"),

# Especialidade Médica
path('cadastrar_especialidade/', views.cadastrar_especialidade, name="cadastrar_especialidade"),
path('listar_especialidade/', views.listar_especialidade, name="listar_especialidade"),
path('editar_especialidade/<int:id>/', views.editar_especialidade, name="editar_especialidade"),
path('remover_especialidade/<int:id>/', views.remover_especialidade, name="remover_especialidade"),

# Exames
path('cadastrar_exame/', views.cadastrar_exame, name="cadastrar_exame"),
path('listar_exame/', views.listar_exame, name="listar_exame"),
path('editar_exame/<int:id>/', views.editar_exame, name="editar_exame"),
path('remover_exame/<int:id>/', views.remover_exame, name="remover_exame"),

# Comprovante
path('comprovante/cirurgia/<int:id>/', views.comprovante_cirurgia, name='comprovante_cirurgia'),
path('comprovante/especialidade/<int:id>/', views.comprovante_especialidade, name='comprovante_especialidade'),
path('comprovante/exame/<int:id>/', views.comprovante_exame, name='comprovante_exame'),
path('agenda/pdf/<int:agenda_id>/', views.pdf_pacientes_agendados, name='pdf_pacientes_agendados'),

# Dashboard
path('remover-usuario/<int:id>/', views.remover_usuario, name='remover_usuario'),

# Agenda
path('criar_agenda/', views.criar_agenda, name="criar_agenda"),
path('agenda/<str:especialidade>/', views.agendas_especialidade, name="agenda_especialidade"),
path('agendar/<int:id>/', views.agendar_paciente, name="agendar_paciente"),

path('remover_paciente_agenda/<int:paciente_id>/', views.remover_paciente_agenda, name='remover_paciente_agenda'),
path('remover_agenda/<int:agenda_id>/', views.remover_agenda, name='remover_agenda'),

]

