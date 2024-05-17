from django.shortcuts import render, redirect, get_object_or_404  #? Funciones para renderizar plantillas, redireccionar y obtener objetos o devolver un 404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  #? Formularios de creación y autenticación de usuarios
from django.contrib.auth.models import User  #? Modelo de usuario de Django
from django.contrib.auth import login, logout, authenticate  # ?Funciones para iniciar sesión, cerrar sesión y autenticar usuarios
from django.contrib.auth.decorators import login_required  #? Decorador para restringir el acceso a usuarios autenticados
from django.db import IntegrityError  #? Excepción para manejar errores de integridad en la base de datos
from .forms import ExpenseForm  #? Importar formulario personalizado de gastos
from .models import Expense  #? Importar el modelo de gastos
from categories.models import Category  #? Importar el modelo de categorías

#----------HOME/LANDING----------#

def home(request):
    if request.user.is_authenticated: #? Si el usuario está autenticado
        return redirect('/expense/') #? redirige al listado de gastos.
    else: #? Sino esta autenticado, lo manda a la landing
        return render(request, "home.html")

# ----------LOGIN AND REGISTER----------#


def signup(request): #? Funcion para registrarse
    if not request.user.is_authenticated: #? Si el usuario está autenticado
        try: #? Bloque para manejar excepciones
            if request.method == 'GET': #? Condicion para verificar si el metodo de la solicitud es 'GET'
                return render(request, "signup.html", { #? Si es 'GET', renderiza el template
                    "form": UserCreationForm #? Se le manda el formulario de registro al template
                })
            else: #? Sino es 'GET' -> es 'POST'
                if request.POST['password1'] == request.POST['password2']: #? Si coinciden las contraseñas
                    try: #? Bloque para manejar excepcion
                        user = User.objects.create_user( #? Se usa el metodo para crear usuario
                            #? Se obtiene el nombre de usuario y la contraseña de la peticion POST
                            username=request.POST["username"], password=request.POST["password1"])
                        login(request, user) #? Se inicia sesion con los datos del usuario
                        return redirect('expense') #? Se redirecciona a los 'Gastos'
                    #? Excepcion que podría ocurrir si se intenta crear un usuario ya existente
                    except IntegrityError: #? 'IntegrityError' se produce cuando se viola la integridad de los datos
                        return render(request, "signup.html", { #? En caso de excepcion renderizar html
                            "form": UserCreationForm, #? Con el formulario de creacion
                            "error": "El usuario ya existe" #? Y el error de que ya existe el usuario
                        })
                return render(request, "signup.html", { #? En caso de que no se cumpla el if se renderiza el signup
                    "form": UserCreationForm, #? Con el formulario de creacion
                    "error": "Las contraseñas no coinciden" #? Y el mensaje de que no cinciden las contras
                })
        except ValueError: #? En caso de excepcion
            return render(request, "signup.html", { #? Se renderiza un error generico
                "form": UserCreationForm,
                "error": "Verifique sus datos"
            })
    else:
         return redirect('/expense/')


def signout(request): #? Funcion para cerrar sesion
    logout(request) #? Funcion para cerrar sesion, requiere de la peticion como argumento
    return redirect("home") #? Redireccion a la pagina de inicio


def signin(request): #? Funcion para iniciar sesion
    if request.method == 'GET': #? Condicion que evalua si el metodo de la solicitud es 'GET'
        return render(request, "signin.html", { #? Si es asi se retorna el template de registro
            "form": AuthenticationForm #? Se manda el formulario de registro importado al template
        })
    else:
        user = authenticate( #? Se usa el metodo importado para autenticar al usuario, devuelve un objeto o none
            request, #? Recibe de argumento la solicitud
            username=request.POST["username"], #? Se manda de argumento el username de la solictud 'POST'
            password=request.POST["password"] #? Se manda de arg la password de la solictud 'POST'
        )
        if user is None: #? Si 'authenticate' no le asigno un obj a 'user', le asigno 'none' pq no existe el usuario
            return render(request, "signin.html", { #? Entonces retornamos el template de login/signin
                "form": AuthenticationForm, #? Con el formulario de login/signin
                "error": "El usuario o la contraseña es incorrecta" #? Mensaje
            })
        else: #? Si le devuelve el objeto de usuario 
            login(request, user) #? Se inicia sesion con el objeto
            return redirect("/expense") #? Se redirecciona a los 'Gastos'

# ----------EXPENSES----------#


# ? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
@login_required
def expense(request): #? Funcion para renderizar los gastos asociados al usuario
    #? Se obtienen los datos de laa tabla de gastos donde la llave foranea user_id sea igual al id del usuario logeado
    expenses = Expense.objects.filter(user_id=request.user)
    return render(request, 'expense.html', { #? Se renderiza el template
        "expenses": expenses, #? Con todos los datos de los gastos del usuario autenticado
    })


# ? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
@login_required
def expense_create(request): #? Funcion para crear gasto
    if request.method == 'GET': #? Condicion de si el metodo de la solicitud es 'GET'
        form = ExpenseForm() #? Instancia del formulario para crear gasto
        #? Del formulario instanciado, en sus campo (field) de categoria se añade una consulta 'queryset'
        form.fields["category_id"].queryset = Category.objects.filter( #? se filtran las categorias
            user_id=request.user) #? Que pertenecen al usuario, para mostrarse
        return render(request, "expense_create.html", { #? Una vez filtrado el fom, se renderiza el html
            'form': form #? Y se manda el formulario
        })
    else: #? Si la solicitud es 'POST'
        try: #? Bloque en caso de excepcion
            form = ExpenseForm(request.POST) #? Instancia del formulario con la solicitud 'POST'
            new_expense = form.save(commit=False) #? Metodo save para obtener los datos que van a guardarse
            new_expense.user_id = request.user #? Se asigna el id del usuario autenticado a la llave foranea 'user_id'
            new_expense.save() #? Y ahora si se guarda en la BD
            return redirect("/expense/") #? Y se redirecciona a los gastos
        except ValueError: #? En caso de error
            return render(request, "expense_create.html", { #? Se renderiza la pagina para crear
                'form': ExpenseForm, #? Con el formulario
                'error': "Verifique los datos ingresados" #? Y un mensaje indicando que hubo un error
            })


# ? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
@login_required
def expense_update(request, expense_id): #? Funcion para actualizar gasto
    if request.method == 'GET': #? Si el metodo de la solictud es 'GET'
        #? Se obtienen los gastos (o error 404), donde el gasto tenga de llave primaria
        #? el id recibido en la solicitud
        expense = get_object_or_404(Expense, pk=expense_id)
        form = ExpenseForm(instance=expense) #? Instancia del formulario llenado con la instancia del dato obtenido
        return render(request, "expense_update.html", { #? Se retorna el template
            "expense": expense, #? Con los datos del gasto obtenido
            "form": form #? Y el formulario llenado con el gasto obtenido
        })
    else: #? De no ser 'GET'
        #? Se obtienen los gastos (o error 404), donde el gasto tenga de llave primaria
        #? el id recibido en la solicitud
        expense = get_object_or_404(Expense, pk=expense_id)
        #? Instancia del formulario llenado con la instancia del dato obtenido y los datos del 'POST'
        form = ExpenseForm(request.POST, instance=expense)
        form.save() #? Se guarda el formulario actualizado
        return redirect("expense") #? Se redirecciona a los 'gastos'


# ? Decorador para proteger ruta / Acceso a la vista solo a usuarios autenticados
@login_required
def expense_delete(request, expense_id): #? Funcion para eliminar gasto, recibe id del gasto
    #? Se obtienen los datos (o error 404) donde la llave primaria sea el id recibido y 
    #? la foranea 'user_id' sea igual al usuario autenticado
    expense = get_object_or_404(Expense, pk=expense_id, user_id=request.user)
    if request.method == "POST": #? Si el metodo es 'POST'
        expense.delete() #? Se elimina el gasto
        return redirect("/expense/") #? Se redirecciona a los gastos
