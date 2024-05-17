"""
El archivo asgi.py en una aplicación de Django es un punto de entrada para las aplicaciones que se 
ejecutan en ASGI (Asynchronous Server Gateway Interface). ASGI es una especificación que permite a las 
aplicaciones web de Python manejar conexiones asincrónicas, lo que es especialmente útil para 
aplicaciones en tiempo real y otras aplicaciones que requieren una gestión eficiente de múltiples 
conexiones.

Para mas informacion:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')

application = get_asgi_application()
