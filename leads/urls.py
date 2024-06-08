from django.urls import path
from .views import (lead_list, lead_detail, lead_create, lead_update, lead_delete, LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView)

app_name = "leads" #Se le tiene que dar un nombre para que se pueda incluir la referencia a este archivo en el urls.py de djcrm. Entonces, cuando alguien entre al url ...leads/..., va a buscar la dirección dentro de esta carpeta

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),#Cuando alguien quiere ingresar al camino default de nuestra página, Django responde con la función home_page establecida en views.py de lead, la cual recibe un request y se ejecuta de acuerdo a lo establecido

    path('create/', LeadCreateView.as_view(), name='lead-create'),

    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),#cuando se introduzca una llave primaria en el path del url, este llama a la vista lead_detail para mostrar la información de aquel lead que corresponda con la llave primaria ingresada

    #Tenemos que poner el path de '<pk>/' hasta abajo para que django no interprete que cualquier otro path es una llave primaria. O podemos establecer que una llave primaria es un numero entero, de esta manera django solo accede al path '<pk>/' si es un entero
    path('<int:pk>/update/', LeadUpdateView.as_view(), name= 'lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete')
]

#Con el name=... se le da un nombre al url, y lo que nos permite esto es referenciar cada uno de los paths de manera más facil. Por ejemplo, en los templates, si se quiere colocar un <a href"..."></a>, se puede colocar el nombre del path que asignamos en caso que el "hard-coded link" se llegue a modificar