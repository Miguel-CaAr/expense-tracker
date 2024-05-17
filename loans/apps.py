from django.apps import AppConfig

""" 
Configuración y personalización de la aplicación.
Permite definir el nombre de la aplicación y configuraciones 
adicionales que pueden ser necesarias para el correcto funcionamiento de la aplicación.
"""
class LoansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loans'
