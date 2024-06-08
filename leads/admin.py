from django.contrib import admin

from .models import User, Lead, Agent, UserProfile

'''Nos permite mostrar nuestros modelos en la página de administrador de Django de nuestra aplicación web'''

admin.site.register(User)
admin.site.register(UserProfile) #Registramos nuestro UserProfile
admin.site.register(Lead)
admin.site.register(Agent)