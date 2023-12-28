# GUIA DE LOGUIN USANDO UN API DE MICROSOFT


# CREAMOS UNA APLICACIÓN EN EL PORTAL DE AZURE

Crearemos una nueva aplicacion para ello entramos a https://portal.azure.com/

<div>
<img style="height: 200px;" src="img/img_26.png">
</div>

Nuevo Registro

<div>
<img style="height: 200px;" src="img/img_27.png">
</div>

Agregamos un nombre 

<div>
<img style="height: 200px;" src="img/img_28.png">
</div>

Agregamos la plataforma web **Importante que sea Web** por que en otras plataformas nos pediran claves PKCE entre otros.

<div>
<img style="height: 200px;" src="img/img_29.png">
</div>

agregamos una dirección URL de redirección `http://localhost:8000/oauth2/callback`para entenderlo `oauth2` esta definido en el archivo `url.py` en nuestro proyecto en django y `callback` es una dirección interna de django_auth_adfs, asi que no debemos cambiarla.

y en la dirección de cierre pusimos una con el protocolo https cualquiera, y seguro que da error pero mas adelante lo cambiaremos, esta solo es de prueba.

<div>
<img style="height: 200px;" src="img/img_30.png">
</div>

Copiamos el ID del cliente.

`53c79f5a-1a55-484c-a60f-4ba7f8a8b2b7`

<div>
<img style="height: 200px;" src="img/img_31.png">
</div>

Creamos el secreto de cliente.

<div>
<img style="height: 200px;" src="img/img_32.png">
</div>

Copiamos el secreto de cliente nada mas crearlo, por que luego se ocultara para siempre.

`wTU8Q~MNTgPGN8SQO5_Q9bVk1qSOwGp7zn2zUcte`

<div>
<img style="height: 200px;" src="img/img_33.png">
</div>

Copiamos el tenant_id o tambien llamado el id directorio (inquilino)

`5ce759eb-f346-49c8-a506-f8839107ec38`

<div>
<img style="height: 200px;" src="img/img_34.png">
</div>

## IMPLEMENTAMOS LA API CON DJANGO

He de decir que para implementar el API con mi app de Django solo necesitamos las tres llaves de las credenciales, y sincronizar la url de destino que debuelve al iniciar sesión.

### INSTALAMOS django-auth-adfs PARA LA AUTENTICACIÓN CON AZURE

    pip install django-auth-adfs

Una vez ya instalado lo agregamos en nuestro `archivo settings.py`

```py
INSTALLED_APPS = [
    ...
    'django_auth_adfs',
]
```

### ALGUNAS CONFIGURACIONES DE SETTINGS.PY

```py
# VARIABLES DE REDIRECCIÓN DE LOGIN Y LOGOUT
LOGIN_REDIRECT_URL = 'http://localhost:8000/'
# LOGOUT_REDIRECT_URL = 'n_home'

#SETTINGS FOR LOGIN WITH MICRFOSOFT

AUTHENTICATION_BACKENDS = (
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Configure django to redirect users to the right URL for login
LOGIN_URL = "django_auth_adfs:login"
LOGIN_REDIRECT_URL = "/"
```

### INSTALAMOS python-dotenv PARA MANEJAR ALGUNAS VARIABLES

`python-dotenv` Nos sirve para manejar variables delicadas y poder interactuar con ellas apartado de nuestro archivo de configuración, son buenas practicas.

Asi que lo instalaremos para manejar las variables de las credenciales.

    pip install python-dotenv

Luego creamos el archivo donde estaran las variables `\mysite\.env`.

Y agregamos estas variables.

~~~
client_id = '53c79f5a-1a55-484c-a60f-4ba7f8a8b2b7'

client_secret = 'wTU8Q~MNTgPGN8SQO5_Q9bVk1qSOwGp7zn2zUcte'

tenant_id = '5ce759eb-f346-49c8-a506-f8839107ec38'
~~~

Ahora importamos el anterior archivo `.env` en `settings.py`

```py
import os
from dotenv import load_dotenv
load_dotenv()

# Client secret is not public information. Should store it as an environment variable.
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
tenant_id = os.getenv("tenant_id")
```

Implementamos las variables en `AUTH_ADFS` y con eso ya finalizamos las configuración de nuestro archivo `setting.py`

```py
AUTH_ADFS = {
    'AUDIENCE': client_id,
    'CLIENT_ID': client_id,
    'CLIENT_SECRET': client_secret,
    'CLAIM_MAPPING': {'first_name': 'given_name',
                      'last_name': 'family_name',
                      'email': 'upn'},
    'GROUPS_CLAIM': 'roles',
    'MIRROR_GROUPS': True,
    'USERNAME_CLAIM': 'upn',
    'TENANT_ID': tenant_id,
    'RELYING_PARTY_ID': client_id,
}

# CON LOS PRINTS COMPROBAREMOS SI LAS VARIABLES CONTIENEN ALGO
print("260 IQ")
print(client_secret)
```

### url.py Y LOGIN and LOGOUT

Como dije anteriormente la ruta `oauth2` es importante ya que debemos usar esa misma en la redirección de nuestra app de azure

```py
urlpatterns = [
    path('oauth2/', include('django_auth_adfs.urls')),
]
```

A las vistas que se necesiten acceder logueados deberemos de poner el siguiente decorator.

La vista que tenga el decorator nos redireccionara al login de Microsoft

`myapp/views.py`

```py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
def hello(request):
    return render(request,'home.html')

@login_required
def products(request):
    return render(request,'productos.html')

def exit(request):
    logout(request)
    print("Hola")
    return redirect('n_home')
```

`myapp/url.py`

```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='n_home'),
    path('init/', views.products, name='n_products'),
    path('logout/', views.exit, name='n_exit'),
]
```

Con la etiqueta `salir` cerramos sesión

La etiqueta `Ingresar` no nos sirve (es parte del sistema de loguin de django pero para el login de microsoft no nos sirve)

Nos logueamos con la etiqueta `Productos` Por que nos redirecciona al loguin con Microsoft

Tambien tenemos el if y el else de django que nos sirve tambien para el loguin con Microsoft.

`myapp/templates/base.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aplicación</title>
</head>
<body>
    <h2>Inicio</h2>
    <ul>
        <li><a href="{% url 'n_home' %}">Inicio</a></li>
        <li><a href="{% url 'n_products' %}">Productos</a></li>

        {% if request.user.is_authenticated %}
        <li><a href="{% url 'n_exit' %}">Salir</a></li>
        {% else %}
        <li><a href="{% url 'login' %}">Ingresar</a></li>
        {% endif %}

    </ul>
    {% block content %}
    {% endblock %}
</body>
</html>
```

Aqui vemos como obtener el username, nos sirve tambien par el loguin con Microsoft.

`myapp/templates/home.html`

```html
{% extends 'base.html' %}

{% block content %}
<h3>Inicio</h3>
<hr>
<h1>Bienvendo {{ user.username }}</h1>
{% endblock %}
```

## CONSENTIMIENTO DE ADMINISTRADOR PARA LA API

No tenemos concentimiento en la app de esta guia

<div>
<img  src="img/img_36.png">
</div>

Es por eso que nos sale este error al terminar de loguearnos *(si nos permite loguearnos pero una vez logueados nos sale este error)*

<div>
<img  src="img/img_35.png">
</div>
<div>
<img  src="img/img_37.png">
</div>

Con mi correo de estudiante no tengo permisos para `conceder consentimiento` es por eso que le pedi al director de la institucion educativa `ILS` me cediera los consentimientos en una App que creé previamente.

<div>
<img  src="img/img_38.png">
</div>

Ahora si que todo esta correcto.

<div>
<img  src="img/img_39.png">
</div>
<div>
<img  src="img/img_40.png">
</div>
<div>
<img  src="img/img_41.png">
</div>
<div>
<img  src="img/img_42.png">
</div>
<div>
<img  src="img/img_43.png">
</div>

## LINKS - BIBLIOGRAFIA

> Video tutorial de un marroqui del que me gue para poder hacer el login

- Video "grd7qqj295_vid.mp4" ➡️ [Link vídeo](./video/grd7qqj295_vid.mp4)

> Documentación original de `django_auth_adfs`

https://django-auth-adfs.readthedocs.io/en/latest/install.html

> Portal de Azure

https://portal.azure.com/#home

> Proyecto de login `log_api_microsoft` en github

https://github.com/Edgar-ae/log_api_microsoft