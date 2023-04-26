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

Para Python, he utilizado la imagen Docker `python:3.9.13-alpine3.16` que tiene Alpine y Python instalado (puede verse en su [Dockerfile](https://github.com/docker-library/python/blob/a2ed46f4405e35ddd583deb6001b7a90bb1bd810/3.11-rc/alpine3.16/Dockerfile)); al tenerlo todo en la imagen Docker se puede comparar el total que necesitaría el programa con Python.

Pese a que con el binario en Rust es suficiente para ejecutar el programa sin instalar nada mas, creo que es interesante mostrar el tamaño en cada parte (construir binario, ejecutar en Docker y tamaño del binario) por varios motivos:

- Si llevo el binario a un sistema que no sea Alpine, ya habría que usar Docker o construir el binario para ese sistema, lo que implica instalar lo necesario para ello, así creo que se tiene una idea del espacio total. Por ejemplo, en un sistema Debian, el binario ocupa un poco menos, 3,9 MB, pero para construirlo necesito tener instalado otro software.
- Como Python no tiene binario, con Docker sería el modo de comparar el tamaño.

Puede ser una ventaja de Python, que teniendo en cuenta el espacio total, ganaría Python, pero eliminando partes no necesarias para lanzar el programa al final sí que se ocupa menos con Rust.


## Links de este tutorial

- [Página principal](introduction.html)
- [Siguiente apartado. Comparar tiempo de ejecución](08-compare-execution-time.html)

