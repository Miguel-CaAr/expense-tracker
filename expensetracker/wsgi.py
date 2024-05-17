"""
WSGI significa "Python Web Server Gateway Interface". Es una especificación de estándar de Python 
que describe cómo los servidores web pueden comunicarse con aplicaciones web escritas en Python, como 
las aplicaciones Django.

El propósito principal de WSGI es proporcionar una interfaz común entre los servidores web y las 
aplicaciones web, lo que permite que diferentes servidores web y marcos de aplicaciones se comuniquen 
entre sí de manera eficiente.

Para mas informacion:
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')

application = get_wsgi_application()
