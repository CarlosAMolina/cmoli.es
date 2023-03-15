# Configurar los proyectos


## Introducción 

Tras haber comentado las partes del programa, llega la hora de prepararlo para poder ejecutarlo :)

En este apartado configuraremos los proyectos necesarios y en el siguiente los lanzaremos.

## Crear carpeta de trabajo

Como a lo largo de estas entradas trabajaremos con diferentes proyectos y archivos, crearemos una carpeta donde almacenarlo todo.

```bash
mkdir -p ~/Software/poc-rust
cd ~/Software/poc-rust
```

## Obtener archivos de logs

El primer paso es disponer de logs que convertir a .csv ¿No tienes estos archivos? Ningún problema, con el siguiente programa (escrito en Rust, por supuesto ;)) podemos generar archivos de logs rápidamente.

Descargamos el programa y accedemos a su carpeta:

```bash
git clone https://github.com/CarlosAMolina/nginx-logs-generator
cd nginx-logs-generator
```

Crearemos en la ruta `~/Software/poc-rust/logs/` los siguiente archivos de logs:

- access.log.2.gz, 110 MiB (1.4 GiB sin comprimir).
- access.log.1, 477 MiB.
- access.log, 954 MiB.

Para ello, con el siguiente comando, indicamos la ruta de destino (el programa creará la carpeta llamada `logs`), y el tamaño de los archivos (en Gigabytes):

```bash
cargo run ~/Software/poc-rust 1.5 0.5 1
```

Ya con esto, volvemos a nuestra ruta principal de trabajo:

```bash
cd ~/Software/poc-rust
```

## Programa para convertir logs a csv

El programa que utilizaremos para convertir nuestros archivos de logs a csv puede descargarse con el siguiente comando:

```bash
git clone https://github.com/CarlosAMolina/nginx-logs
cd nginx-logs
```

### Configurar versión en Python

Para trabajar con la versión Python del programa, solamente hay que acceder a la carpeta con el código, no es necesario instalar ninguna librería externa.

Ejecutando el programa con el argumento `-h` obtenemos un texto de ayuda:

```bash
$ cd python
$ python src/main.py -h
usage: main.py [-h] pathname

Export Nginx logs to a csv file.

positional arguments:
  pathname    path to a folder with the log files or to an specific file

options:
  -h, --help  show this help message and exit
```

### Configurar versión en Rust

Al igual que hemos lanzado la versión Python de este programa, para Rust, accedemos a la carpeta con el código en este lenguaje y lo ejecutamos, en este caso sin utilizar ningún argumento.

En lugar de obtener un texto de ayuda como en Python, en Rust no se ha implementado esto y simplemente se mostrará con un error que no se ha proporcionado el argumento pathname.

```bash
$ cd ~/Software/poc-rust/nginx-logs/rust
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.11s
     Running `target/debug/nginx_logs`
Problem parsing arguments: No pathname provided
```

## Recursos

Programa para generar logs:

<https://github.com/CarlosAMolina/nginx-logs-generator>

Programa para convertir logs a csv:

<https://github.com/CarlosAMolina/nginx-logs>

## Links de este tutorial

- [Página principal](introduction.html)

