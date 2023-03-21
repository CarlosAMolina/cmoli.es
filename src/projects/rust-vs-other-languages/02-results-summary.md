# Resumen de los resultados

## Contenidos

- [Introducción](#introducción)
- [Espacio en disco](#espacio-en-disco)
- [Tiempo de ejecución](#tiempo-de-ejecución)
- [Memoria](#memoria)
- [CPU](#cpu)
- [Links de este tutorial](#links-de-este-tutorial)

## Introducción

En este apartado se mostrarán los resultados de comparar Rust con otros lenguaje de programación. El objetivo es mostrar un resumen inicial y, en los siguientes capítulos ir obteniendo estas conclusiones paso a paso y analizarlas.

## Espacio en disco

Para conocer el tamaño necesario se utiliza Docker para crear el entorno que trabaje con el programa.

Comparando la versión Rust del programa con su versión en Python, los resultados son los siguientes:

Lenguaje | Tamaño    | Descripción
---------|-----------|--------------------------------------------------
Rust     | 2.83 GB   | Tamaño para compilar el archivo binario y ejecutarlo.
Rust     | 15.39 MB  | Tamaño para ejecutar el binario, es decir, si ya tenemos el programa compilado, es el espacio que necesitaría el archivo binario y una imagen Docker que pueda ejecutarlo.
Rust     | 4.1 MB    | Tamaño del binario. De tener un sistema compatible puede utilizarse este binario en lugar de Docker y así sería necesario aún menos espacio.
Python   | 94,8 MB   |

Imágenes Docker utilizadas:

- Python: python:3.9.13-alpine3.16.
- Rust: imagen rust:1.62.1-slim para compilación y alpine:3.16 para ejecutar el binario.

## Tiempo de ejecución

Lenguaje | Tiempo (ms)
---------|------------
Rust     |   4
Python   |   54

## Memoria

- Heap

![](metrics-memory-massif-rust-heap-only.png)

> Memoria heap Rust

![](metrics-memory-massif-python-heap-only.png)

> Memoria heap Python

- Heap y stack

![](metrics-memory-massif-rust-add_stacks.png)

> Memoria heap y stack Rust

![](metrics-memory-massif-python-add_stacks.png)

> Memoria heap Python

- Page level

![](metrics-memory-massif-rust-add-pages-as-heap.png)

> Memoria page level Rust

![](metrics-memory-massif-python-add-pages-as-heap.png)

> Memoria page level Python

## CPU

![](metrics-cpu-rust.png)

> CPU Rust

![](metrics-cpu-python.png)

> CPU Python

## Links de este tutorial

- [Página principal](introduction.html)
- [Siguiente apartado. Especificaciones del equipo](03-host-specifications.html)

