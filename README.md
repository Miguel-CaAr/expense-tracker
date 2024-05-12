## Crear un entorno virtual

### El comando para incializar/crear un entorno virtual (se usa -m abreviatura a --module)
```bash
python3 -m venv nombre_entorno
```

### El comando para activar el entorno virtual (primero en Unix/Linux, despues Windows)
```bash
source ./venv/bin/activate #Mac Os
./venv/Scripts/activate #Windows
```
## Instalacion de Django y dependencias
```bash
pip3 install -r ./requirement.txt
```
## Recoleccion de archvios estaticos
```bash
python3 manage.py collectstatic
```
## Ejecucion
```bash
python3 manage.py runserver
```