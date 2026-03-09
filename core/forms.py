from django import forms
from .models import PacienteCirurgia, PacienteEspecialidade, PacienteExame

class PacienteCirurgiaForm(forms.ModelForm):
    class Meta:
        model = PacienteCirurgia
        fields = ["nome", "sus", "telefone", "ubs", "agente_saude", "cirurgia"]

class PacienteEspecialidadeForm(forms.ModelForm):
    class Meta:
        model = PacienteEspecialidade
        fields = ["nome", "sus", "telefone", "ubs", "agente_saude", "especialidade"]

class PacienteExameForm(forms.ModelForm):
    class Meta:
        model = PacienteExame
        fields = ["nome", "sus", "telefone", "ubs", "agente_saude", "exame"]