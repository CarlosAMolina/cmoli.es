# Comparar espacio en disco

## Contenidos

- [Introducción](#introducción)
- [Configuración](#configuración)
- [Proceso](#proceso)
  - [Elegir imágenes Docker](#elegir-imágenes-docker)
  - [Trabajar con las imágenes Docker](#trabajar-con-las-imágenes-docker)
    - [Rust](#rust)
    - [Python](#python)
- [Comparación tamaños y conclusiones](#comparación-tamaños-y-conclusiones)
- [Recursos](#recursos)
- [Links de este tutorial](#links-de-este-tutorial)

## Introducción

Gracias a que Rust crea un ejecutable del programa, puede utilizarse en otro equipo que no tenga Rust instalado, siempre que el archivo ejecutable sea compatible. En cambio, con Python es necesario tener instalado este lenguaje en el equipo donde lanzar el programa.

Por tanto, para comparar el tamaño requerido en cada lenguaje, se ha estudiado lo siguiente:

- Tamaño que ocupa la instalación del lenguaje. Esto aplica a Rust y Python.
- Espacio que necesitaría un entorno capaz de iniciar el ejecutable, sin tener instalado el lenguaje. Solamente aplica a Rust ya que en el caso de Python hace falta tenerlo instalarlo.
- Conocer únicamente el tamaño del archivo ejecutable. Este último punto aplica solamente a Rust; es interesante saber cuánto ocuparía el programa de haberlo creado para una arquitectura específica.

Conocer el tamaño requerido se realiza con Docker; gracias al sistema de contenedores, tendremos la información del tamaño utilizado.

## Configuración

Para trabajar con Docker, he instalado Docker Engine, puede seguirse este [link](https://docs.docker.com/engine/install/#other-linux-distros); en mi caso, utilizo el modo [rootless](https://docs.docker.com/engine/security/rootless/) para que no sean necesarios permisos de administrador.

## Proceso

Primero, escogemos las imágenes Docker necesarias, tras lo cual crearemos nuestras imágenes y compararemos su tamaño.

### Elegir imágenes Docker

Las imágenes Docker son las correspondientes a las versiones de los lenguajes que instalamos previamente, utilizaremos las que permitan lanzar el programa utilizando el mínimo espacio posible:

- En Rust elegimos [rust:1.69.0-slim-buster](https://hub.docker.com/_/rust) para crear el archivo ejecutable, y [alpine:3.17.3](https://hub.docker.com/_/alpine) para lanzarlo. Como indica el [archivo de configuración de rust:1.69.0-slim-buster](https://github.com/rust-lang/docker-rust/blob/35579d26bda862c00d127d63cee4ab9cd5d114c2/1.69.0/buster/slim/Dockerfile), las versiones empleadas son Rust 1.69.0 y Debian buster-slim. El tamaño de las imágenes puede verse en el [apartado de tags](https://hub.docker.com/_/rust/tags); como curiosidad, pese a que Alpine se caracteriza por ser la opción de menor tamaño, el tamaño de la versión 1.69.0-alpine3.17 para AMD es de 259.84 MB comprimidos, mientras que la 1.69.0-slim-buster es menor, 234.92 MB.
- Respecto a Python, trabajaremos con [python:3.11.3-alpine3.17](https://hub.docker.com/_/python); puede verse en su [archivo de configuración](https://github.com/docker-library/python/blob/2bcce464bea3a9c7449a2fe217bf4c24e38e0a47/3.11/alpine3.17/Dockerfile) que utiliza la versión de Alpine 3.17 y Python 3.11.3. En el [apartado de tags](https://hub.docker.com/_/python/tags) se muestran los tamaños de cada imagen.

### Trabajar con las imágenes Docker

En el [proyecto](https://github.com/CarlosAMolina/nginx-logs/) que transforma logs de Nginx a csv, hay disponibles unos scripts en bash con los comandos necesarios para trabajar con Docker.

#### Rust

En el caso de Rust, como se indicó al inicio de este apartado, el tamaño necesario puede enfocarse de varias maneras dependiendo de la situación; podemos estudiar el tamaño total para compilar el ejecutable y lanzarlo, el tamaño de un entorno que permita iniciar el ejecutable, o simplemente el tamaño del archivo ejecutable.

Para obtener estas imágenes, se utiliza la opción [multi-stage de Docker](https://docs.docker.com/build/building/multi-stage/), con la cual podemos crear por un lado la imagen para crear el archivo ejecutable y por otro la imagen con el entorno que lo lanzará.

Vamos al directorio de trabajo que nos permite crear las imágenes Docker y volumen para guardar archivos de logs a analizar. Para ello:

```bash
$ cd  ~/Software/nginx-logs/rust/
$ ./run-docker -b
...
Step 9/10 : RUN ls -lh nginx_logs
 ---> Running in 78d5618eaac1
-rwxr-xr-x    1 root     root        4.5M Apr 29 17:00 nginx_logs
...
```

Como se observa, se incluyó en el archivo Dockerfile una línea que muestra el tamaño del archivo ejecutable durante la creación de la imagen, se indica que ocupa 4.5MB.

En el archivo Dockerfile puede verse también cómo se instalan los requisitos para crear un archivo ejecutable que pueda utilizarse en Alpine.

Las imágenes creadas han sido:

```bash
$ docker image ls
REPOSITORY        TAG                  IMAGE ID       CREATED              SIZE
rust-nginx-logs   latest               05fc08c40000   54 seconds ago       11.8MB
<none>            <none>               6e25dae7f156   About a minute ago   1.45GB
rust              1.69.0-slim-buster   675ffb14bc3e   8 days ago           735MB
alpine            3.17.3               9ed4aefc74f6   4 weeks ago          7.04MB
```

El tamaño ha sido:

- La imagen con todo lo necesario para crear el ejecutable: 1.45GB, una vez creado el ejecutable puede eliminarse esta imagen, no es necesaria para trabajar con el.
- Imagen para lanzar el archivo ejecutable: 11.8MB.
- Tamaño del ejecutable (se mostró anteriormente durante la creación de la imagen): 4.5MB

Podemos confirmar que el programa funciona, copiamos un archivo de logs cualquiera al volumen e iniciamos el archivo ejecutable:

```bash
$ cp  ~/Software/poc-rust/logs/access.log ~/.local/share/docker/volumes/nginx-logs-volume/_data/
$ ./run-docker -r
[DEBUG] Init run
Checking: logs
File with logs as csv: logs/result.csv
File with not parsed logs: logs/error.txt
Init file: logs/access.log
...
```

#### Python

Primero, eliminamos las imágenes Docker creadas hasta ahora, para poder ver claramente las que construiremos en este apartado:

```bash
docker image rm -f $(docker image ls -q)
```

Cambiamos el directorio de trabajo y creamos la imagen Docker con los archivos necesarios y el volumen en el que guardar los logs a analizar:

```bash
$ cd  ~/Software/nginx-logs/python/
$ ./run-docker -b
```

Los pasos para crear la imagen pueden verse en el archivo Dockerfile del anterior directorio.

Verificamos que se puede trabajar con esta imagen de Docker, para ello copiamos un archivo de logs al volumen Docker, y lanzamos una ejecución:

```bash
$ cp  ~/Software/poc-rust/logs/access.log ~/.local/share/docker/volumes/nginx-logs-volume/_data/
$ ./run-docker -r
[DEBUG] Init run
Checking: logs
File with logs as csv: logs/result.csv
File with not parsed logs: logs/error.txt
Init file: logs/access.log
...
```

Como vemos, el proceso es correcto, ahora revisamos el tamaño de las imágenes creadas:

```bash
$ docker image ls
REPOSITORY          TAG                 IMAGE ID       CREATED         SIZE
python-nginx-logs   latest              67b3dd268c10   8 minutes ago   51.8MB
python              3.11.3-alpine3.17   8a7f410141c5   3 weeks ago     51.8MB
```

El tamaño requerido por nuestra imagen llamada `python-nginx-logs` es de 51.8MB.

## Comparación tamaños y conclusiones

Los tamaños de las imágenes Docker han sido:

Lenguaje | Tamaño | Imagen Docker            | Descripción
---------|--------|--------------------------|----------------------------------------------------------------
Rust     | 1.45GB | rust:1.69.0-slim-buster  | Imagen para compilar el archivo ejecutable y lanzarlo.
Rust     | 11.8MB | alpine:3.17.3            | Imagen de un sistema capaz de lanzar el archivo ejecutable.
Rust     | 4.5MB  | -                        | Tamaño de archivo ejecutable a utilizar en sistemas compatibles.
Python   | 51.8MB | python:3.11.3-alpine3.17 | Tamaño del lenguaje para lanzar el programa.

Si no tenemos en cuenta el tamaño para compilar y crear el archivo ejecutable, Rust es mejor opción que Python ya que, podemos trabajar con el ejecutable directamente en un sistema compatible necesitando solamente 4.5MB o, si el sistema no fuera compatible con el ejecutable, este podría utilizarse gracias a la imagen Alpine, requiriendo 11.8MB.

En cambio, si pensamos en el espacio para crear el ejecutable, en Rust nos iríamos a 1.45GB de tamaño, lo que es una peor opción que los 51.8MB de Python.

## Recursos

Docker Engine:

<https://docs.docker.com/engine/install/#other-linux-distros>

Docker imágenes:

<https://hub.docker.com>

Docker modo rootless:

<https://docs.docker.com/engine/security/rootless/>

Docker opción multi-stage:

<https://docs.docker.com/build/building/multi-stage/>

Programa para convertir logs a csv:

<https://github.com/CarlosAMolina/nginx-logs>

## Links de este tutorial

- [Siguiente apartado. Comparar tiempo de ejecución](08-compare-execution-time.html)
- [Página principal](introduction.html)

