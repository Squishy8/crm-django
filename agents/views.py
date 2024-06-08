import random
from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        #Esta parte toma el usuario que esta logeado. La parte de userprofile toma al Modelo UserProfile del usuario que esta logeado. La relación que tiene esto en el agente es de una llave foránea al modelo UserProfile. De esta manera se van a filtrar los agentes de acuerdo con el campo de organisation
        return Agent.objects.filter(organisation=organisation)#Podemos filtrar nuestros agentes de acuerdo con 2 campos definidos en el modelo de agente: user y organisation. "Regresame los objetos de agente, en los cuales el organisation es igual al organisation del usuario que los está solicitando"
    
class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView): #Esta vista va a crear un usuario y automáticamente crea al agente, enviándole un  correo confirmando su incorporación al equipo
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(100000,1000000000)}") #El valor que se encuentra adentro del paréntesis debe ser un string. En nuestro caso elegimos una contraseña default aleatoria. set_password automáticamente hashea la contraseña
        user.save()
        Agent.objects.create( #Una vez que se guarda el usuario, se guarda el agente con el usuario igual al usuario creado, y la organisasion igual a la del usuario que está creando el perfil.
            user=user,
            organisation= self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent!",
            message="You were added as an agent on DJCRM. Please login to start working",
            from_email = "admin@test.com",
            recipient_list = [user.email],
        )
        #agent.organisation = self.request.user.userprofile #Se guarda el agente debajo del userprofile que lo está creando
        #agent.save()
        return super(AgentCreateView, self).form_valid(form)
    
class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent" #Especificamos el context object para que sea agent

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list") #CADA VEZ QUE VAYAMOS A CREAR, MODIFICAR O ELIMINAR ALDO DE UN QUERYSET DE LA BASE DE DATOS, DEBEMOS PROPORCIONAR UN GET_SUCCESS_URL PARA QUE SE LLEVE A CABO DE LA MANERA ADECUADA
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent" #Especificamos el context object para que sea agent

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)