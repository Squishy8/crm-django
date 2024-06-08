from django.test import TestCase #Django busca los tests aquí adentro y los ejecuta todos
from django.shortcuts import reverse

'''Este archivo se utilizará únicamente para testear las vistas'''

class LandingPageTest(TestCase): #Va a testear la vista de LandingPageView para asegurarse de que esté ejecutandose correctamente

#Si se crea un método en cualquier clase que sea del tipo test, si lo defines como "def test_..." se ejecutará el código de el mismo como un solo test
    def test_status_code(self):
        #TODO some sort of test
        response = self.client.get(reverse("landing-page")) #Se utiliza self.client para hacerle un request

        #reverse() nos permite utilizar el nombre del path en vez de tener que colocar todo el path textual

        #Lo que nos da el chorizo anterior es la respuesta de utilizar el path "landing-page", lo cual es un html

        self.assertEqual(response.status_code, 200) #Compara el response.status_code de response, que es self.client.get(reverse("landing-page")), y lo compara con el status_code 200 para verificar que todo se esté ejecutando de manera correcta. De no ser igual a 200 entonces tenemos un error
        self.assertTemplateUsed(response, "landing.html") #Corrobora que el template que se está obteniendo con el get es el de "landing.html"

        '''Para correr un test utilizamos python manage.py test'''