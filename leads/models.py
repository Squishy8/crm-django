from django.db import models
from django.db.models.signals import post_save #Este método se llama una vez que la información se haya guardado en la base de datos. pre_save sirve para agregar información nueva justo antes de que sea comprometida dentro de la base de datos
from django.contrib.auth.models import AbstractUser 
#es una funcion para obtener el modelo usuario que ofrece django

class User(AbstractUser): #Checamos si el usuario es un organisator, y si lo es le mostramos cierta información, y si no lo es entonces no le mostramos cierta info
    is_organisor = models.BooleanField(default=True) #Una vez que creas una nueva cuenta, por default eres un organisador, y si creas un agente entonces automáticamente se asigna que es un agente
    is_agent = models.BooleanField(default=False)

    #Vamos a querer mostrar el link de los Agentes a aquellos usuarios que son organisators, pero no a los que son agentes

class UserProfile(models.Model): #Va a estar ligado con un usuario, vamos a ligar un agente a cada UserProfile padre respectivo para que esté gobernado bajo el mismo UserProfile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #Si un usuario crea una cuenta solo puede tener un perfil, no pueden tener más.
    #La iformación de first_name y last_name se obtendrán del modelo User, por ende no tenemos que especificar esos atributos dentro de el modelo UserProfile

    def __str__(self):
        return self.user.username

'''Heredamos de AbstractUser para crear nuestra propia clase usuario para poder agregar nuevos campos si asi lo requerimos. Como por ejemplo agregar un númeor telefónico'''

'''La llave foránea te permite relacionar una tabla con otra'''
class Agent(models.Model):

    '''Como el agente si se va a logear dentro del sistema le asignamos un usuario'''

    '''The OneTooOneField indicates that every agent has one user asigned to them'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #Si el UserProfile es eliminado, entonces todos los agentes para ese perfil serán eliminados de igual forma

    def __str__(self):
        return self.user.email

'''Se crea un modelo que va a ser una tabla dentro de una base de datos. Esta tabla pertenece a la app Leads'''
class Lead(models.Model):

    '''Estas son las opciones que puede elegir el campo de "source". Estas restricciones no limitan lo que se puede meter a la base de datos, es mas bien una restricción de python'''
    #SOURCE_CHOICES = (
        #'''El primer valor es el que se almacena en la base de datos, y el segundo valor es el que se mostrará'''

        #('Youtube','Youtube'),
        #('Google', 'Google'),
        #('Newsletter','Newsletter'),
    #)
    
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default = 0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #Agregamos este campo al lead para que en caso de que no tenga un agente asignado si tenga en todo momento una organisation a la que pertenezca. De esta manera no permitimos que la categorización de Leads dependa solamente del agente al que se asignen.
    agent = models.ForeignKey("Agent", null = True, blank=True, on_delete=models.SET_NULL)

    #Ahora, si tenemos un  agente asignado a un Lead y decidimos eliminar a ese agente no se eliminarán los leads que estaban asignados a el, únicamente se quedará en null el valor del campo correspondiente

    '''agent es la llave foránea que hace referencia a la tabla de AGENT. Cada lead tiene un agente'''

    '''models.CASCADE: Si se elimina un agente relacionado con un lead, se elimina el lead igualmente

    models.SET_NULL, null=True: Si se elimina un agente relacionado con el lead, el campo obtiene un valor de NULL
    
    models.SET_DEFAULT, default = ***: Si se elimina un agente relacionado con el lead, el campo obtiene un valor default determinado por nosotros en el apartado de "default= ***"'''

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    #phoned = models.BooleanField(default=False)

    '''Podemos establecer que un campo en la base de datos solo tenga una cierta cantidad de opciones de las que puede elegir, por ello creamos SOURCE_CHOICES. Este campo nos dice de donde se consiguió el lead'''
    #source = models.CharField(choices=SOURCE_CHOICES, max_length=100)


    '''Blank refiere que puedes meter un valor que sea un String vacío, Null quiere decir que no existe un valor. En esencia es opcional que haya o no una foto de perfil'''
    #profile_picture = models.ImageField(blank=True, null=True)

    '''Este archivo no se guarda directamente en la base de datos, lo que se guarda es una referencia a la ubicación del archivo'''
    #special_files = models.FileField(blank=True, null=True)


'''SIGNALS'''
def post_user_created_signal(sender, instance, created, **kwargs): #El primer parámetro es el sender; el segundo es instance, siendo este el modelo que se guardó (User en este caso); created nos indica si se creó o no el modelo (True o False) y **kwargs el cual captura todos los demás argumentos en caso de haberlos
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)
        #Esta condicional comprueba si se creó o no un usuario, para lo cual, en caso de ser verdadero, se crea un perfil de usuario usando la instancia (username de User) como user
    pass

    #queremos llamar esta función una vez se reciba el evento post_save


post_save.connect(post_user_created_signal, sender=User)

#Se toma la señal, la cual tiene un método "connect", el cual toma el nombre de la función que queremos llamar y el modelo exacto que envía el evento. Es decir, una vez que se guarde un User, django manda la señal post_save y ejecuta la función que queramos utilizar (en exte caso post_user_created_signal)
