from django.contrib import admin
from .models import PacienteCirurgia, PacienteEspecialidade, PacienteExame

# ---------------------- Paciente Cirurgia ----------------------
@admin.register(PacienteCirurgia)
class PacienteCirurgiaAdmin(admin.ModelAdmin):
    list_display = (
        "criado_por",
        "hora_cadastro",
        "nome",
        "sus",
        "telefone",
        "ubs",
        "agente_saude",
        "cirurgia",
        "protocolo",
    )
    list_filter = ("ubs", "cirurgia", "criado_por")
    search_fields = ("nome", "sus", "telefone", "protocolo")

# ---------------------- Paciente Especialidade Médica ----------------------
@admin.register(PacienteEspecialidade)
class PacienteEspecialidadeMedicaAdmin(admin.ModelAdmin):
    list_display = (
        "criado_por",
        "hora_cadastro",
        "nome",
        "sus",
        "telefone",
        "ubs",
        "agente_saude",
        "especialidade",
        "protocolo",
    )
    list_filter = ("ubs", "especialidade", "criado_por")
    search_fields = ("nome", "sus", "telefone", "protocolo")

# ---------------------- Paciente Exame ----------------------
@admin.register(PacienteExame)
class PacienteExameAdmin(admin.ModelAdmin):
    list_display = (
        "criado_por",
        "hora_cadastro",
        "nome",
        "sus",
        "telefone",
        "ubs",
        "agente_saude",
        "exame",
        "protocolo",
    )
    list_filter = ("ubs", "exame", "criado_por")
    search_fields = ("nome", "sus", "telefone", "protocolo")