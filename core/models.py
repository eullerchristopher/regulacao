from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Max

UBS_CHOICES = [
    ("Centro 1", "Centro 1"),
    ("Centro 2", "Centro 2"),
    ("Sertãozinho 1", "Sertãozinho 1"),
    ("Sertãozinho 2", "Sertãozinho 2"),
    ("Jiqui 1", "Jiqui 1"),
    ("Jiqui 2", "Jiqui 2"),
    ("Areia Branca 1", "Areia Branca 1"),
    ("Areia Branca 2", "Areia Branca 2"),
    ("Areia Branca 3", "Areia Branca 3"),
    ("Lagoa de São João", "Lagoa de São João"),
    ("Barra do Cunhaú", "Barra do Cunhaú"),
    ("Outeiro", "Outeiro"),
    ("Piquiri 1", "Piquiri 1"),
    ("Piquiri 2", "Piquiri 2"),
    ("Piquiri 3", "Piquiri 3"),
    ("Meira Lima 1", "Meira Lima 1"),
    ("Meira Lima 2", "Meira Lima 2"),
    ("Regulação", "Regulação")
]

CIRURGIA_CHOICES = [
    ("Cabeça e Pescoço","Cabeça e Pescoço"),
    ("Ginecologia","Ginecologia"),
    ("Hérnia","Hérnia"),
    ("Vesícula","Vesícula"),
    ("Ortopédica","Ortopédica"),
    ("Urológica","Urológica"),
    ("Pediátrica","Pediátrica"),
    ("Neurológica","Neurológica"),
    ("Pequena Cirurgia","Pequena Cirurgia"),
    ("Cardíaca","Cardíaca"),
    ("Plástica","Plástica"),
]

ESPECIALIDADE_CHOICES = [
    ("Cardiologista","Cardiologista"),
    ("Dermatologista","Dermatologista"),
    ("Endocrinologista","Endocrinologista"),
    ("Ginecologista","Ginecologista"),
    ("Mastologista","Mastologista"),
    ("Neurologista","Neurologista"),
    ("Ortopedista","Ortopedista"),
    ("Urologista","Urologista"),
    ("Cir. Vascular","Cir. Vascular"),
    ("Gastroenterologista","Gastroenterologista"),
    ("Reumatologista","Reumatologista"),
    ("Oftalmologista","Oftalmologista"),
    ("Otorrinolaringologista","Otorrinolaringologista"),
]

EXAME_CHOICES = [
    ("Ultrassonografia","Ultrassonografia"),
    ("Endoscopia","Endoscopia"),
    ("Ecocardiograma","Ecocardiograma"),
    ("Tomografia","Tomografia"),
    ("Ressonância","Ressonância"),
]

# ---------------------- PACIENTE CIRURGIA ----------------------
class PacienteCirurgia(models.Model):
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    hora_cadastro = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=200)
    sus = models.CharField(max_length=15)
    telefone = models.CharField(max_length=20)
    ubs = models.CharField(max_length=50, choices=UBS_CHOICES)
    agente_saude = models.CharField(max_length=100, blank=True)
    cirurgia = models.CharField(max_length=50, choices=CIRURGIA_CHOICES)
    protocolo = models.CharField(max_length=50, blank=True, unique=True)
    def save(self, *args, **kwargs):
        if not self.protocolo:
            ano = now().year
            ultimo_protocolo = PacienteCirurgia.objects.filter(
                protocolo__contains=f"CIR-{ano}"
            ).aggregate(Max('protocolo'))['protocolo__max']

            if ultimo_protocolo:
                numero = int(ultimo_protocolo.split('-')[-1]) + 1
            else:
                numero = 1

            self.protocolo = f"CIR-{ano}-{numero:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

# ---------------------- PACIENTE ESPECIALIDADE ----------------------
class PacienteEspecialidade(models.Model):
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    hora_cadastro = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=200)
    sus = models.CharField(max_length=15)
    telefone = models.CharField(max_length=20)
    ubs = models.CharField(max_length=50, choices=UBS_CHOICES)
    agente_saude = models.CharField(max_length=100, blank=True)
    especialidade = models.CharField(max_length=50, choices=ESPECIALIDADE_CHOICES)
    protocolo = models.CharField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.protocolo:
            ano = now().year
            ultimo_protocolo = PacienteEspecialidade.objects.filter(
                protocolo__contains=f"ESP-{ano}"
            ).aggregate(Max('protocolo'))['protocolo__max']

            if ultimo_protocolo:
                numero = int(ultimo_protocolo.split('-')[-1]) + 1
            else:
                numero = 1

            self.protocolo = f"ESP-{ano}-{numero:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

# ---------------------- PACIENTE EXAME ----------------------
class PacienteExame(models.Model):
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    hora_cadastro = models.DateTimeField(auto_now_add=True)
    nome = models.CharField(max_length=200)
    sus = models.CharField(max_length=15)
    telefone = models.CharField(max_length=20)
    ubs = models.CharField(max_length=50, choices=UBS_CHOICES)
    agente_saude = models.CharField(max_length=100, blank=True)
    exame = models.CharField(max_length=50, choices=EXAME_CHOICES)
    protocolo = models.CharField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.protocolo:
            ano = now().year
            ultimo_protocolo = PacienteExame.objects.filter(
                protocolo__contains=f"EXA-{ano}"
            ).aggregate(Max('protocolo'))['protocolo__max']

            if ultimo_protocolo:
                numero = int(ultimo_protocolo.split('-')[-1]) + 1
            else:
                numero = 1

            self.protocolo = f"EXA-{ano}-{numero:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
# ---------------------- AGENDA ----------------------
class Agenda(models.Model):

    STATUS_CHOICES = [
        ("andamento", "Em andamento"),
        ("finalizada", "Finalizada"),
    ]
    especialidade = models.CharField(max_length=50, choices=ESPECIALIDADE_CHOICES)
    data = models.DateField()
    total_vagas = models.IntegerField()
    vagas_por_ubs = models.IntegerField()
    vagas_regulacao = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="andamento"
    )
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)


    # Vagas restantes totais da agenda
    def vagas_restantes(self):
        usadas = sum([ubs.vagas_usadas for ubs in self.agendaubs_set.all()])
        return self.total_vagas - usadas

    # Total de vagas usadas na agenda
    def total_vagas_usadas(self):
        return sum([ubs.vagas_usadas for ubs in self.agendaubs_set.all()])

    # verificar se agenda lotou
    def agenda_lotada(self):

        return self.vagas_restantes() <= 0

    # verificar status automaticamente
    def verificar_status(self):

        hoje = now().date()

        # finaliza se a data já passou
        if self.data < hoje:
            self.status = "finalizada"
            self.save()
            return

        # finaliza se lotar
        if self.agenda_lotada():
            self.status = "finalizada"
            self.save()

    def __str__(self):

        return f"{self.especialidade} - {self.data}"
    
# ---------------------- VAGAS UBS ----------------------

class AgendaUBS(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    ubs = models.CharField(max_length=50, choices=UBS_CHOICES)
    vagas = models.IntegerField()
    vagas_usadas = models.IntegerField(default=0)

    def vagas_restantes(self):
        return self.vagas - self.vagas_usadas

    def __str__(self):
        return f"{self.ubs} - {self.agenda.especialidade} ({self.vagas_restantes()} vagas restantes)"


# ---------------------- AGENDAMENTO PACIENTE ----------------------
class AgendamentoPaciente(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    ubs = models.CharField(max_length=50, choices=UBS_CHOICES)
    nome = models.CharField(max_length=200)
    sus = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    agente = models.CharField(max_length=150)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Novo campo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # verificar se agenda lotou
        self.agenda.verificar_status()

    def __str__(self):
        return f"{self.nome} - {self.ubs} - {self.agenda.especialidade}"
