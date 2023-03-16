# Programa desarrollado

## Contenidos

- [Introducción](#introducción)
- [Partes](#partes)
- [Recursos](#recursos)
- [Links de este tutorial](#links-de-este-tutorial)

## Introducción 

El programa que estudiaremos transforma los archivos de logs de un servidor Nginx en un único archivo `csv`. De este modo, es mas fácil su análisis al poder separar su contenido en columnas, filtrar valores, etc.

El código del programa está disponible en el siguiente [enlace](https://github.com/CarlosAMolina/nginx-logs).

## Partes

Las acciones realizadas por el programa son:

- Recibir por línea de comandos los valores dados por el usuario.
- Ordenar los archivos de logs a analizar desde el más antiguo hasta el más actual para que en el archivo `csv` resultante los logs aparezcan en orden cronológico.
- Separar con coma las partes de cada log y exportar este resultado en un archivo final.

## Recursos 

Programa que convierte archivos de logs en `csv`:

<https://github.com/CarlosAMolina/nginx-logs>

## Links de este tutorial

- [Página principal](introduction.html)
- [Siguiente apartado. Instalación Rust y Python](02-installation-rust-and-python.html)

