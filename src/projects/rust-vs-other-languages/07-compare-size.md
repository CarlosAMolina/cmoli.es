# Comparar espacio en disco

## Introducción

Rust es un lenguaje que, tras compilar el programa, el archivo ejecutable resultante puede utilizarse en otro equipo que no tenga Rust instalado.

En cambio, con Python es necesario tener instalado este lenguaje en el equipo donde lanzar el programa.

Tamaños necesaros:

- Python (imagen Docker `python:3.9.13-alpine3.16`): 94,8 MB.
- Rust (imagen Docker `rust:1.62.1-slim` para compilación y `alpine:3.16` para ejecutar el binario):
  - 2,83 GB de imágenes Docker para construir el binario y ejecutarlo.
  - 15,39 MB de imágenes Docker para ejecutar el binario. Esto se obtiene tras eliminar las imágenes que se crearon para su compilación pero que ya no son necesarias.
  - 4.1 MB es el tamaño del binario, por lo que de tener un sistema compatible puede utilizarse este binario en lugar de Docker y así sería necesario aún menos espacio.

## Links de este tutorial

- [Página principal](introduction.html)
- [Siguiente apartado. Comparar tiempo de ejecución](08-compare-execution-time.html)

