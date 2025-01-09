# Python. Importar una clase de diferentes modos genera distintos objetos

## Contenidos

- [Introducción](#introducción)
- [Resumen del motivo](#resumen-del-motivo)

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
from src.main import run
```

Para que la excepción fuera capturada, el test debía hacer el `import` de esta manera:

```python
# test_main.py
from src.main import FolderInS3UriError
from src.main import run
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
|  |__exception.py
|__main.py
```

```python
# exception.py
class CustomError(IsADirectoryError):
    pass
```

```python
# main.py
import pathlib
import sys

from subfolder.exceptions import CustomError as FromSubfolderCustomError

# Modificar sys.path para hacer el import de otra manera.
sys.path.append(str(pathlib.Path(__file__).parent.absolute().joinpath("subfolder")))

from exceptions import CustomError as FromFileCustomError


# Comprobar que la clase importada de diferente manera no captura la excepción.
# El siguiente código hace print de `Captured by FromFileCustomError`.
try:
    raise FromFileCustomError()
except FromSubfolderCustomError:
    print("Captured by FromSubfolderCustomError")
except FromFileCustomError:
    print("Captured by FromFileCustomError")

# Las instancias no tienen relación con la clase importada de diferente manera.
assert not isinstance(FromFileCustomError(), FromSubfolderCustomError)
assert not isinstance(FromSubfolderCustomError(), FromFileCustomError)

# Diferentes imports generan diferentes objetos.
assert FromFileCustomError is not FromSubfolderCustomError

# Mostrar en qué se diferencias las clases
print(FromSubfolderCustomError)  # <class 'subfolder.exceptions.CustomError'>
print(FromFileCustomError)  # <class 'exceptions.CustomError'>

# Los datos anteriores nos dicen que se han cargado distintos módulos.
print(sys.modules["subfolder.exceptions"])  # <module 'subfolder.exceptions' from '/tmp/src/subfolder/exceptions.py'>
print(sys.modules["exceptions"])  # <module 'exceptions' from '/tmp/src/subfolder/exceptions.py'>
```

Con esto tengo importadas las dos situaciones, la que captura la excepción y la que no, de modo que puedo analizar sus diferencias. En el código anterior en lugar de trabajar con `try-except` se utiliza `isinstance`, ahora veremos por qué.

### Funcionamiento de try-except

El problema es que la cláusula `except` no capturaba la excepción, por lo que el primer paso es entender qué hace `except`. Como indica la [documentación oficial](https://docs.python.org/3/tutorial/errors.html).

> A class in an except clause matches exceptions which are instances of the class itself or one of its derived classes.

Es decir, la excepción no capturada es porque no es una instancia de la clase que aparece tras `except`. Para saber si una clase es instancia de otra, tenemos la función [isinstance](https://docs.python.org/3/library/functions.html#isinstance); en el código anterior se muestra que clases importadas de diferentes modos no son instancias unas de otras.

Esto es lo que no comprendía; si ambas clases vienen del mismo archivo `exceptions.py`, yo pensaría que se tratan del mismo objeto por lo que al al instanciarlas unas deberían ser instancias de otras, pero no es así.

### ¿Por qué el import afecta a las clases?

Para comprender la diferencia entre las clases, hay que obtener información de ellas, puede utilizarse la función `type` pasándole una instancia de la clase, pero he trabajado con `print` y las clases sin inicializar (muestra la misma información que daría `type()`):

```python
print(FromSubfolderCustomError)  # <class 'subfolder.exceptions.CustomError'>
print(BFromSubfolderCustomError)  # <class 'subfolder.exceptions.CustomError'>
print(FromFileCustomError)  # <class 'exceptions.CustomError'>
```

Como se ve, las clases importadas como `from subfolder.exceptions import CustomError as ...`, tiene el mismo valor `subfolder.exceptions.CustomError` a pesar de haber utilizado un alias al importarlas; pero la clase importada mediante `from exceptions import CustomError as ...` tiene un valor diferente, `exceptions.CustomError`.

¿Qué significan los valores `subfolder.exceptions.CustomError` y `exceptions.CustomError`? Se trata del módulo cargado y el nombre de la clase en ese módulo, aunque no he encontrado documentación que lo diga directamente, puede verificarse esto con la función `sys.modules`:

```python
print(sys.modules["subfolder.exceptions"]) # <module 'subfolder.exceptions' from '/tmp/src/subfolder/exceptions.py'>
print(sys.modules["exceptions"]) # <module 'exceptions' from '/tmp/src/subfolder/exceptions.py'>
```

Aclarar que la función anterior `sys.modules`, [da la siguiente información](https://docs.python.org/3/library/sys.html#sys.modules):

> This is a dictionary that maps module names to modules which have already been loaded

Aquí está la clave, la clase importada de diferentes maneras pertenece a módulos diferentes, y cada uno tiene su propio namespace independiente, como explica la [documentación oficial](https://docs.python.org/3/tutorial/modules.html):

> Each module has its own private namespace

Además, vemos en [la documentación oficial](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces) los namespaces no tienen relación entre ellos:

> there is absolutely no relation between names in different namespaces

Aclarar que un namespace es ([link a documentación](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)):

> A namespace is a mapping from names to objects

La información obtenida hasta ahora nos muestra que la misma clase importada de distintas maneras, `from subfolder.exceptions import CustomError as ...` y `from exceptions import CustomError as ...`, produce objetos diferentes.

Terminar indicando qué hace la parte `from ... import ...`, podemos revisarlo en la [documentación](https://docs.python.org/3/tutorial/modules.html):

> There is a variant of the import statement that imports names from a module directly into the importing module’s namespace. For example: from fibo import fib, fib2

Con todo esto, la conclusión es que, en nuestro namespace, hemos importado las clases `FromSubfolderCustomError` y `FromFileCustomError`, pero están asociadas a diferentes módulos; como en cada módulo pertenecen a un namespace diferente, no tienen relación entre ellas y son objetos distintos, no habiendo relación entre ellos, lo que impide que unos capturen a los otros en `try-except`.

### ¿Afectan los alias?

Si con lo visto hasta ahora me llevo la idea de que diferentes imports crean distintos objetos, empiezo a dudar si los alias también impactan. Por suerte no es así ;).

Puede verse en este código:

```python
from subfolder.exceptions import CustomError as FromSubfolderCustomError
from subfolder.exceptions import CustomError as BFromSubfolderCustomError

assert FromSubfolderCustomError is BFromSubfolderCustomError
assert isinstance(FromSubfolderCustomError(), BFromSubfolderCustomError)
```

Podemos ver cómo un alias no cambia el objeto ya que tienen el mismo ID, el ID se muestra con la función [id()](https://docs.python.org/3/library/functions.html#id), y pueden compararse los IDs con la función [is](https://docs.python.org/3/reference/expressions.html#is-not).

Al tratarse del mismo objeto, también se cumple la función `isinstance`.

## Conclusión

Gracias a este análisis he podido comprender mejor funciones de Python como `id, `isinstance` o `type`, y otros aspectos de Python como los módulos y namespaces.
