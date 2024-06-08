
from django.conf import settings #Usando esta importación podemos hacer referencia a las variables como STATIC_URL y STATIC_ROOT
from django.conf.urls.static import static #Esta es una función que acepta dos cosas
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
    )
from django.urls import path, include #ayuda a incluir el método include, que nos permite incluir la dirección del archivo urls.py de una app en específico
from leads.views import landing_page, LandingPageView, SignupView #importamos la vista del landing page de leads

'''urlpatterns es una lista de paths que existen en nuestra
aplicación web, indicando qué vista debe encargarse de eses path'''

'''Cuando una persona mete un url de nuestra página, se busca el path proporcionado en esta lista para ejecutar la función que se estableció como segundo argumento'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('leads/', include('leads.urls', namespace="leads")), 
    #Si alguien entra al path leads/ de nuestra página, django va a buscar dentro de la carpeta leads el archivo urls que se encuentra en el archivo leads.
    path('agents/', include('agents.urls', namespace="agents")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), #La vista revisa que uidb64 y token estén en el url, de lo contrario lanza un error. NECESITA TENER AMBOS EN UN URL PARA QUE SEA VÁLIDO PODER CAMBIAR LA CONTRASEÑA
    path('password-reset-complete', PasswordResetCompleteView.as_view(), name='password_reset_complete') 
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)