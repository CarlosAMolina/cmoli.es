# Python. Importar una clase de diferentes modos genera distintos objetos

## Contenidos

- [Contenidos](#contenidos)
- [Introducción](#introducción)
- [Resumen del motivo](#resumen-del-motivo)
- [Análisis](#análisis)
  - [Preparar el laboratorio](#preparar-el-laboratorio)
  - [Funcionamiento de try-except](#funcionamiento-de-try-except)
  - [Mostrar diferencia entre las clases importadas](#mostrar-diferencia-entre-las-clases-importadas)
  - [¿Afectan los alias?](#¿afectan-los-alias?)
- [Conclusión](#conclusión)

## Introducción

En estos días me topé con una de esas situaciones en que el código no se comporta como esperaba; tras varios intentos de prueba y error, conseguí el funcionamiento deseado, pero no entendía el motivo... Tocó estudiar Python en profundidad :).

El programa donde ocurrió esto consiste en listar los archivos de AWS S3; pero si detecta una carpeta, genera una excepción para finalizar la ejecución y mostrar un mensaje de aviso, ya que de momento no puede analizar subdirectorios. Esta excepción es una propia llamada `FolderInS3UriError`, y se detecta con un bloque `try-except`:

```python
# main.py
from exceptions import FolderInS3UriError


try:
    run()
except FolderInS3UriError as exception:
    show_folder_error_message(exception)
```

Al hacer peticiones contra AWS, el funcionamiento era el esperado, e incluso escribí un test que demostraba que el bloque `except FolderInS3UriError` capturaba la excepción, para ello el test hacía peticiones a un servidor local que simula AWS S3. Pero quería agilizar el test evitando iniciar el servidor local, por lo que gracias a `unittest.mock` modificaría `run()` para generar la excepción.

Es con este mock donde el comportamiento era extraño; la excepción no era capturada por el bloque try-except. El problema ocurría en test, cuando importaba la excepción a mockear de este modo:

```python
# test_main.py
from src.exceptions import FolderInS3UriError
```

Para que la excepción fuera capturada, el test debía hacer el `import` de esta manera:

```python
# test_main.py
from src.main import FolderInS3UriError
```

¿Por qué afecta importarlo de una manera u otra? Al fin y al cabo la clase importada se encuentra en el mismo archivo `exceptions.py`, no comprendía qué ocurre en Python para que esto modificara el capturar la excepción.

## Resumen del motivo

Para que no haga falta leer todo el artículo, aquí resumo la conclusión. En los siguientes apartados se explicará el análisis con más detalle.

Hay que tener claros varios puntos para comprender el motivo:

- Cada módulo posee un `namespace` diferente y los objetos que contiene no tienen relación con los objetos de otros módulos.
- El bloque try-except captura excepciones que son instancias de la clase indicada o de alguna clase hija.

Al importar la excepción `FolderInS3UriError` de diferentes maneras, Python la asocia a módulos diferentes y el objeto mockeado desde el archivo de test no tiene relación con el utilizado en la cláusula `except FolderInS3UriError` del archivo main, por lo que la excepción no era capturada.

Muy resumida esta es la conclusión, ahora veremos un ejemplo con una explicación más detallada donde paso a paso llegaremos a esta conclusión.

## Análisis

El primer paso fue escribir un código con el que poder hacer pruebas para comprender cada parte involucrada.

### Preparar el laboratorio

Aunque podía modificar el proyecto original, prefería llevar la situación a estudiar a un proyecto diferente, así podía hacer modificaciones libremente y guardar comentarios que consultar a futuro.

Una vez duplicado el proyecto original en uno de prueba, trabajé con el código que provocaba el error (que la excepción mockeada no se capturase) y eliminé todo el código que no afectara a esto.

Acabé con este pequeño proyecto:

```bash
src
|__subfolder
|  |__exceptions.py
|__main.py
```

```python
# exceptions.py
class CustomError(IsADirectoryError):
    pass
```

```python
# main.py
import pathlib
import sys

from subfolder.exceptions import CustomError as FromSubfolderCustomError

# Modify sys.path to make a different import.
sys.path.append(str(pathlib.Path(__file__).parent.absolute().joinpath("subfolder")))

from exceptions import CustomError as FromFileCustomError


# The class imported in a different way does not capture the exception.
# The following code prints `Captured by FromFileCustomError`.
try:
    raise FromFileCustomError()
except FromSubfolderCustomError:
    print("Captured by FromSubfolderCustomError")
except FromFileCustomError:
    print("Captured by FromFileCustomError")

# No instances relation between classes imported in a different way.
assert not isinstance(FromFileCustomError(), FromSubfolderCustomError)
assert not isinstance(FromSubfolderCustomError(), FromFileCustomError)

# Different imports generate different objects.
assert FromFileCustomError is not FromSubfolderCustomError

# Show the difference between classes.
print(FromSubfolderCustomError)  # <class 'subfolder.exceptions.CustomError'>
print(FromFileCustomError)  # <class 'exceptions.CustomError'>

# The previous data means that different modules were loaded.
print(sys.modules["subfolder.exceptions"])  # <module 'subfolder.exceptions' from '/tmp/src/subfolder/exceptions.py'>
print(sys.modules["exceptions"])  # <module 'exceptions' from '/tmp/src/subfolder/exceptions.py'>

# Classes are different objects.
assert FromFileCustomError is not FromSubfolderCustomError
```

Con este código he simulado el error, la excepción no se captura si no se importa de determinada manera. Gracias a este pequeño código he podido replicar el error y escribir nuevo código que me permite estudiar el porqué; lo comentamos en los siguientes apartados.

### Funcionamiento de try-except

El objetivo es comprender por qué la cláusula `except` no capturaba la excepción; por tanto, el primer paso es entender cómo funciona la cláusula `except`. Como indica la [documentación oficial](https://docs.python.org/3/tutorial/errors.html).

> A class in an `except` clause matches exceptions which are instances of the class itself or one of its derived classes.

Es decir, la excepción no capturada es porque no es una instancia de la clase que aparece tras `except`. Para saber si una clase es instancia de otra, tenemos la función [isinstance](https://docs.python.org/3/library/functions.html#isinstance); en el código anterior se muestra que clases importadas de diferentes modos no son instancias unas de otras.

Aquí tenemos la primera pista, aunque ambas clases vienen del mismo archivo `exceptions.py`, al inicializarlas unas no son instancias de otras. ¿Qué diferencia hay entre las clases?

### Mostrar diferencia entre las clases importadas

Ya hemos visto que las clases no son iguales, obtengamos información de ellas para conocer el motivo.

Para esto, puede utilizarse la función `type()` pasándole una instancia de la clase, pero he trabajado con `print()` ya que muestra los mismos datos que `type()` sin utilizar como argumentos las clases inicializadas:

```python
# from subfolder.exceptions import CustomError as FromSubfolderCustomError
print(FromSubfolderCustomError)  # <class 'subfolder.exceptions.CustomError'>

# from exceptions import CustomError as FromFileCustomError
print(FromFileCustomError)  # <class 'exceptions.CustomError'>
```

Como se ve, las clases muestran diferentes valores `subfolder.exceptions.CustomError` y `exceptions.CustomError` pero, ¿qué significado tienen? Se trata del módulo cargado y el nombre de la clase en ese módulo, aunque no he encontrado documentación que lo especifique directamente, puede verificarse con la función `sys.modules`:

```python
print(sys.modules["subfolder.exceptions"])  # <module 'subfolder.exceptions' from '/tmp/src/subfolder/exceptions.py'>
print(sys.modules["exceptions"])  # <module 'exceptions' from '/tmp/src/subfolder/exceptions.py'>
```

Aclarar que la función anterior `sys.modules`, [ofrece la siguiente información](https://docs.python.org/3/library/sys.html#sys.modules):

> This is a dictionary that maps module names to modules which have already been loaded.

Aquí está la clave, la clase importada de diferentes maneras pertenece a módulos diferentes. El siguiente punto importante es que cada módulo tiene su propio namespace, como explica la [documentación oficial](https://docs.python.org/3/tutorial/modules.html):

> Each module has its own private namespace.

Además, vemos en [la documentación oficial](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces) que los namespaces no tienen relación entre ellos:

> There is absolutely no relation between names in different namespaces.

Aclarar que, un namespace es ([link a documentación](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)):

> A namespace is a mapping from names to objects.

Recapitulemos la información obtenida hasta ahora: la misma clase importada de distintas maneras, `from subfolder.exceptions import CustomError as FromSubfolderCustomError` y `from exceptions import CustomError as FromFileCustomError`, produce objetos diferentes.

Verificamos que son objetos diferentes al tener distinto ID, el ID se muestra con la función [id()](https://docs.python.org/3/library/functions.html#id), y los IDs pueden compararse con la función [is](https://docs.python.org/3/reference/expressions.html#is-not):

```python
# Classses are different objects.
assert FromFileCustomError is not FromSubfolderCustomError
```

Solo faltaría aclarar que la parte `from ... import ...`, realiza lo siguiente ([documentación](https://docs.python.org/3/tutorial/modules.html)):

> There is a variant of the `import` statement that imports names from a module directly into the importing module’s namespace. For example: from fibo import fib, fib2

Con todo esto, la conclusión es que, en nuestro namespace, hemos importado las clases `FromSubfolderCustomError` y `FromFileCustomError`, pero están asociadas a diferentes módulos; como en cada módulo pertenecen a un namespace diferente, no tienen relación entre ellas y son objetos distintos. Al no haber relación entre estos objetos, unos no pueden capturar a otros en el bloque `try-except`.

### ¿Afectan los alias?

Hay que tener claro que, la diferencia que afecta al hacer los imports es en la ruta del módulo importado; los alias no modifican las clases importadas:

```python
# alias.py
from subfolder.exceptions import CustomError as FromSubfolderCustomError
from subfolder.exceptions import CustomError as BFromSubfolderCustomError

assert FromSubfolderCustomError is BFromSubfolderCustomError
assert isinstance(FromSubfolderCustomError(), BFromSubfolderCustomError)
```

Podemos ver cómo un alias no cambia el objeto ya que tienen el mismo ID; al tratarse del mismo objeto, también se cumple la función `isinstance`.

## Conclusión

Gracias a este análisis pude entender mejor las importaciones en Python, los módulos y sus namespaces; así como el funcionamiento de los bloques `typ-except` utilizados tan habitualmente, y las funciones `isinstance()` o `type()`.
