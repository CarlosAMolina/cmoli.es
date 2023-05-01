# Resumen de los resultados

## Contenidos

## Introducción

En este apartado se mostrarán los resultados de comparar Rust con otros lenguaje de programación. El objetivo es mostrar un resumen inicial y, en los siguientes capítulos ir obteniendo estas conclusiones paso a paso y analizarlas en mayor profundidad.

## Espacio en disco

Para conocer el tamaño necesario se utiliza Docker para crear el entorno que trabaje con el programa.

Comparando la versión Rust del programa con su versión en Python, los resultados son los siguientes:

Lenguaje | Tamaño | Imagen Docker            | Descripción
---------|--------|--------------------------|----------------------------------------------------------------
Rust     | 1.45GB | rust:1.69.0-slim-buster  | Imagen para compilar el archivo ejecutable y lanzarlo.
Rust     | 11.8MB | alpine:3.17.3            | Imagen de un sistema capaz de lanzar el archivo ejecutable.
Rust     | 4.5MB  | -                        | Tamaño de archivo ejecutable a utilizar en sistemas compatibles.
Python   | 51.8MB | python:3.11.3-alpine3.17 | Tamaño del lenguaje para lanzar el programa.

## Archivos a analizar

Los ficheros de logs que convertiremos a un archivo csv y así comparar las características de cada lenguaje como el tiempo de ejecución necesario y el uso de memoria y CPU, han sido:

-  12M access.log
- 7,1M access.log.1
- 692K access.log.2.gz
- 976K access.log.3.gz
- 1,3M access.log.4.gz
- 827K access.log.5.gz
- 902K access.log.6.gz
- 557K access.log.7.gz
- 826K access.log.8.gz
- 902K access.log.9.gz

El número total de líneas de logs a analizar es de 551.692.

## Tiempo de ejecución

Al procesar los archivos de logs antes indicados, se ha tenido lo esperado, Rust es mucho más rápido que Python:

![](execution-time.png)

> Media tiempo de ejecución

Las dos primeras columnas son los resultados más rápidos en cada lenguaje. Con Rust se consigue parseando cada parte del log buscando las posiciones que indican el fin de cada una, no se emplean expresiones regulares; mientras que, en Python se utiliza la función `match` con una expresión regular que obtiene todos los elementos del log guardados en grupos.

Como curiosidad, se han añadido las dos últimas columnas donde vemos que, en Rust el programa es más lento con expresiones regulares, e incluso puede llegar a tardar más que la versión de Python según la función de búsqueda empleada.

## Memoria

Se han realizado 3 mediciones para cada programa, el uso de memoria heap, uso de memoria heap y stack, y uso de toda la memoria (lo llamo page level); se explican estas opciones más detalladamente en el apartado dedicado al estudio de la memoria utilizada.

Rust presenta un menor consumo que Python, el comentario de las gráficas puede verse en el apartado del análisis de la memoria. Los resultados han sido:

- Heap

![](metrics-memory-massif-rust-heap-only.png)

> Memoria heap Rust

![](metrics-memory-massif-python-heap-only.png)

> Memoria heap Python

- Heap y stack

![](metrics-memory-massif-rust-add_stacks.png)

> Memoria heap y stack Rust

![](metrics-memory-massif-python-add_stacks.png)

> Memoria heap y stack Python

- Page level

![](metrics-memory-massif-rust-add-pages-as-heap.png)

> Memoria page level Rust

![](metrics-memory-massif-python-add-pages-as-heap.png)

> Memoria page level Python

## CPU

Respecto al uso de CPU para convertir los archivos de logs, se tiene:

![](metrics-cpu-rust.png)

> CPU Rust

![](metrics-cpu-python.png)

> CPU Python

Comentar que, el método empleado para medir el uso de CPU no es demasiado correcto, como se explica con mayor detalle en su apartado. Pese a ello, ha servido para obtener estas gráficas y comparar los lenguajes.

## Compilación multiplataforma

Solamente indicar que, pese a ser posible en Rust crear el archivo ejecutable para distintas plataformas, es un proceso no inmediato ya que requiere pasos previos como la instalación de software adicional.

## Otros aspectos

Para terminar, comentamos algunos aspectos a tener en cuenta al trabajar con Rust:

- Tiempo de compilación. Trabajar con lenguajes compilados añade un tiempo de espera cada vez que queramos probar el programa; mientras que, en lenguajes interpretados como Python evitamos esta espera.

## Links de este tutorial

- [Siguiente apartado. Especificaciones del equipo](03-host-specifications.html)
- [Página principal](introduction.html)

