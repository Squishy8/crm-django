from typing import Any
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse #render se encarga de devolver páginas de html, css y javascript
#redirect se encarga de mover al usuario de la página a un path específico despues de que se realice una acción particular
from django.contrib.auth.mixins import LoginRequiredMixin #Esta importación verifica que el usuario actual está autenticado para poder hacer modificaciones. Nos permite restringir acceso
from django.http import HttpResponse #Nos permite regresar información por un request
from django.views import generic #Esto sustituye lo que se encuentra en el comentario de abajo

'''from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView'''

from agents.mixins import OrganisorAndLoginRequiredMixin #Usamos el mixin creado en la app de agents para verificar que un usuario tenga los privilegios correctos para acceder a la información que le compete
from .models import Lead, Agent #importamos el modelo de Lead para acceder a las tablas de la base de datos que se encuentran dentro de ella
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm #Aquí se importa el forms del archivo forms.py


#CRUD - Create, Retrieve, Update and Delete + List
#Toda página siempre va a caer bajo una de estas categorías
#Es recomendable crear clases de vistas utilizando esta metodología CRUD para disminuir la cantidad de código que se tiene que escribir

'''CRUD: Cada una de estas vistas genéricas tiene su propia funcionalidad útil'''


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login") #Nos regresa a la vista de login

class LandingPageView(generic.TemplateView): #Sustituye a def landing_page
    template_name = "landing.html" #El template_name se tiene que especificar en casi todas las vistas genéricas


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin,generic.ListView): #Sustituye a def lead_list
    #LoginRequiredMixin va primero dentro del argumento para asegurarnos que primero se note que el usuario que quiere acceder a esta vista está atuenticado
    template_name = "lead_list.html" #Primero se define el template name
    #queryset = Lead.objects.all()Luego, se establece un query set que queremos enlistar en este template

    #LeastView automaticamente asigna el nombre de la variable de contexto a "object_list", por ende se tiene que colocar esta variable dentro del template para poder llamar a los objetos del modelo Lead

    #Podemos cambiar el nombre de la variable de contexto con "context_object_name = "<nombre de la variable>" "
    context_object_name = "leads"
    def get_queryset(self):
        user = self.request.user #Primero, revisamos quien es el request user (sabemos que tendremos un request.user porque para mostrar esta información se tiene que estar logeado)

        if user.is_organisor: #Revisamos si el usuario es un organisor, porque si son un organisor entonces tienen un userprofile. Accesamos al user profile gracias a la relación entre UserProfile y User en models.py leads. El OneTooOneField nos permite hacer esta relación
            queryset = Lead.objects.filter(organisation= user.userprofile) 
        
        #Con los ifs establecidos en esta funcion, revisamos que el usuario sea un organisor, para entonces mostrar los categorizados bajo el organisation del usuario. De no ser organisor, se muestran únicamente los leads que estan asignados al agente

        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation) #El queryset inicial en este caso se filtra por la organisation a la que está asignado el agente. Usamos agent.ortanisation para obtener su organisation específica, y podemos accesar a agent a través del request.user

            queryset = queryset.filter(agent__user = user) #Estamos filtrando los leads no solo de acuerdo con el agente, si no tambien con el usuario que está logeado en ese momento que se hace la consulta a la base de datos. Entonces, filtramos los leads en donde el usuario de agente asignado a cada Lead sea el mismo que el usuario que solicita la información.
            
            #Si se reasigna un queryset, django no consulta a la base de datos hasta que se regrese el valor del queryset, entonces se pueden hacer asignaciones las veces que se quiera, pero no se va a hacer la consulta hasta el final
        return queryset #Solo cuando se returnea el queryset, django hace el query a la base de datos
            #Django evalúa un queryset

def lead_list(request):
    leads = Lead.objects.all()#obtiene todas las leads y la almacenamos en esta variable. Es un query set
    context = {
        "leads": leads
    }#Utilizamos el context para usarlo dentro del template secong_page.html. Es un diccionario de información a la que podemos acceder

    return render(request, "lead_list.html", context) 

'''la función lead_list recibe el request del url al que está asignado y muestra el html que se encuentra en el folder de "templates" , el cual ya está dado de alta en settings.py en la parte de DIR = []'''

'''Para utilizar esta función, la necesitamos agregar a nuestros url'''

class LeadDetailView(LoginRequiredMixin,generic.DetailView): #Sustituye a def lead_detail
    template_name = "lead_detail.html" 
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user 

        if user.is_organisor: 
            queryset = Lead.objects.filter(organisation= user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation= user.agent.organisation) 
            queryset = queryset.filter(agent__user = user) 
        return queryset 


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk) #Jala una instancia del lead específico y la almacena en la variable
    context = {
        "lead": lead

    }
    return render(request, "lead_detail.html", context)

class LeadCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView): #Sustituye a def lead_create
    template_name = "lead_create.html" 
    form_class = LeadModelForm #Ya no necesitamos el query set en este caso

    def get_success_url(self):
        return reverse("leads:lead-list")#Utilizamos el namespace leads para hacer referencia a los url que se encuentran dentro de l urlpatterns que están dentro de la app leads, en busca del que tenga asignado el nombre lead-list
    
    def form_valid(self, form):
        #TODO send email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"] 
        )#Hacemos que se mande un correo cada vez que se crea un Lead
        return super(LeadCreateView, self).form_valid(form)
    
        #Vamos a hacer que se mande un correo primero, y una vez terminando puede proseguir a hacer lo que estaba haciendo
    
def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save() #Esto hace toda la chamba de lo que está abajo, porque en el LeadModelForm estamos especificando el modelo con el que estamos trabajando, entonces toda la data que pasamos en el form se guradan como una nueva instancia de un lead
            return redirect("/leads")
        #print('Receiving a post request')
        #form = LeadModelForm(request.POST)
        #Si el request que se está pasando es de tipo post, entonces se pasa una instancia de LeadModelForm que permite que se reciban los datos
        #if form.is_valid():
            #Se revisa si la data ingresada en el form es válido, y si lo es se 
        '''print("The form is valid")
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = form.cleaned_data['agent']'''
            #Tomamos la información del form usando cleaned_data
            

        '''Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent
            )'''
            #Con esto se puede cerar un nuevo Lead y pasar la información que proporcionamos en el form
            
    context = {
        "form": form #Creamos una instancia del form
    }
    return render(request, "lead_create.html", context)

class LeadUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView): #Sustituye a def lead_create
    template_name = "lead_update.html"  #Necesitamos pasar un query set
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user 
    
        return Lead.objects.filter(organisation= user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update (request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)#Instance se refiere a la instancia del modelo que queremos actualizar. Si guardamos este form, va a tomar esta instancia y actualizarla en vez de crear una nueva instancia en la base de datos
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context ={
        "form":form,
        "lead": lead
    }

    return render(request, "lead_update.html", context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name="lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user 
    
        return Lead.objects.filter(organisation= user.userprofile)

def lead_delete(request, pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect("/leads")




#REFERENCIA DEL FORM CON LEADFORM
'''def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadForm(request.POST)
        if form.is_valid():
            print("The form is valid")
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first()

            Lead.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                agent=agent
            )
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "lead_create.html", context)'''

#FUNCIÓN UPDATE CON LEADFORM
'''def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm()
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadForm(request.POST)
        if form.is_valid():
            print("The form is valid")
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save() #esto guarda todos los valores anteriores y los guarda a la base de datos
            return redirect("/leads")
    context = {
        "lead": lead,
        "form": form
    }
    return render(request, "lead_update.html", context)'''

