# Introducción al programa desarrollado

## Contenidos

- [Introducción](#introducción)
- [Partes](#partes)
- [Recursos](#recursos)
- [Links de este tutorial](#links-de-este-tutorial)

## Introducción

El programa que estudiaremos transforma los archivos de logs de un servidor Nginx en un único archivo `csv`. De este modo, es mas fácil su análisis al poder separar su contenido en columnas, filtrar valores, etc.

Por ejemplo, un archivo con este contenido:

![](file-logs.png)

> Archivo logs

Será convertido a:

![](file-csv.png)

> Archivo csv

El código del programa está disponible en el siguiente [enlace](https://github.com/CarlosAMolina/nginx-logs).

## Partes

Las acciones realizadas por el programa son:

- Recibir por línea de comandos los valores dados por el usuario, como la ruta con los archivos a convertir.
- Ordenar los archivos de logs a analizar desde el más antiguo hasta el más actual para que, en el archivo `csv` resultante los logs aparezcan en orden cronológico. Es decir, los archivos se analizan en orden de mayor número a menor, por ejemplo, se comienza por `access.log.9.gz`, luego `access.log.8.gz`, etc. y por último `access.log.1` y `access.log`.
- Separar con coma las partes de cada log y exportar este resultado en un archivo final.

## Recursos

Programa que convierte archivos de logs en `csv`:

<https://github.com/CarlosAMolina/nginx-logs>

## Links de este tutorial

- [Siguiente apartado. Resumen de los resultados](02-results-summary.html)
- [Página principal](introduction.html)

