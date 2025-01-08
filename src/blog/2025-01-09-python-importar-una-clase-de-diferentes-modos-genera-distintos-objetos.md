# Python. Importar una clase de diferentes modos genera distintos objetos

## Contenidos

- [Introducción](#introducción)
- [Resumen del motivo](#resumen-del-motivo)

## Introducción

En estos días me topé con una de esas situaciones en que el código no se comportaba como esperaba; tras varios intentos de prueba y error, todo funcionó bien, pero no entendía el motivo... Tocó estudiar el funcionamiento de Python :).

El programa donde tuve el problema realiza peticiones a AWS S3 para listar archivos; pero si detecta una carpeta, generará una excepción para mostrar un mensaje de aviso. Esto se consigue con una excepción propia `FolderInS3UriError` y un bloque `try-except`:

```python
# main.py
from exceptions import FolderInS3UriError

try:
    run()
except FolderInS3UriError as exception:
    show_folder_error_message(exception)
```

Escribí un test que demostraba que la excepción era capturada con `except FolderInS3UriError`, para ello se hacían peticiones a un servidor local que simula AWS S3. Pero quería agilizar el test evitando iniciar el servidor local, por lo que gracias a `unittest.mock` modificaría `run()` para generar la excepción.

Es con este mock donde el comportamiento era extraño; generaba la excepción pero no era capturada por el bloque try-except. El problema ocurría en el archivo de tests cuando importaba la excepción a mockear de este modo:

```python
# test_main.py
from src.exceptions import FolderInS3UriError
```

Para que la excepción fuera capturada, el test debía hacer el `import` de igual manera que en el archivo a testear:

```python
# test_main.py
from src.main import FolderInS3UriError
```

¿Qué más da importarlo de una manera u otra? No comprendía que ocurría en Python para que esto afectara al capturar la excepción, al fin y al cabo la clase importada se encuentra en el mismo archivo `exceptions.py`.

## Resumen del motivo

Para que no haga falta leer todo el artículo, aquí muestro resumida la conclusión. En los siguientes apartados se explicará el análisis con más detalle.

Hay que tener claros varios puntos:

- Al utilizar la sentencia `import` para importar un módulo, cada módulo tiene un `namespace` diferente donde los objetos que contiene no tienen relación con los objetos de otros módulos.
- El bloque try-except captura excepciones que son instancias de la clase indicada o de alguna clase hija.

Como la excepción `FolderInS3UriError` se importa de diferentes maneras, Python la toma de módulos diferentes y el objeto mockeado no tiene relación con el utilizado en la cláusula `except FolderInS3UriError`. Aquí está el motivo de que el modo de importar la clase afecte al mock.

Muy resumida esta es la conclusión, ahora podemos ver paso a paso como llegar a ella.
