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
cd nginx-logs-generator/nginx-logs-generator
```

Ahora, simplemente verificaremos que el programa funciona correctamente:

```bash
$ cargo run
...
Problem parsing arguments: not enough arguments
Usage
    cargo run String Vec<f32>
        The first argument is the path where the `log` folder will be created to save the log files.
        The next arguments are the size (Gigabyte) of each log file to be generated.
    Example:
        cargo run /tmp 1.5 0.5 1

```

Obtenemos mensaje de error porque no hemos proporcionado como argumento el path donde crear los archivos de logs; no supone un problema, ya que solo queríamos lanzar el programa a modo de prueba.

El último paso es crear el archivo ejecutable de este programa, conviene hacer una breve explicación de los comandos utilizados:

- Con la orden `cargo run` el programa es compilado, utilizando la orden `cargo build`, y también se lanza el ejecutable resultante, el cual se guarda en la carpeta `target/debug`, con el nombre del programa, `nginx-logs-generator` en este caso. Este es un ejecutable creado rápidamente para probar el programa mientras desarrollamos.
- Con la orden `cargo build --release` compilamos el programa con optimizaciones que harán que funcione a mayor velocidad. El comando `cargo build` generaba un ejecutable sin optimizaciones, que es mas rápido de compilar, por lo que es más conveniente durante el desarrollo del programa, aunque es más lento en ejecución. El ejecutable resultado será creado en `target/relase`.

Por tanto, generamos el ejecutable con:

```bash
cargo build --relase
```

Si comparamos los archivos resultantes de `cargo build` y `cargo build --release` vemos que el programa con optimizaciones ocupa menos espacio:

```bash
$ ls -lh target/debug/nginx-logs-generator
8,6M target/debug/nginx-logs-generator
[x@arch nginx-logs-generator]$ ls -lh target/release/nginx-logs-generator
4,3M target/release/nginx-logs-generator
```

Puede ejecutarse del siguiente modo:

```bash
$ ./target/release/nginx-logs-generator
Problem parsing arguments: not enough arguments
Usage
    cargo run String Vec<f32>
        The first argument is the path where the `log` folder will be created to save the log files.
        The next arguments are the size (Gigabyte) of each log file to be generated.
    Example:
        cargo run /tmp 1.5 0.5 1
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

Al igual que hemos lanzado la versión Python de este programa, para Rust, accedemos a la carpeta con el código en este lenguaje y lo ejecutamos, en este caso sin utilizar ningún argumento. Se mostrará con un error que no se ha proporcionado el argumento pathname, y un texto de ayuda.

```bash
$ cd ~/Software/poc-rust/nginx-logs/rust
$ cargo run
   ...
   Compiling nginx_logs v0.1.0 (/tmp/nginx-logs/rust)
    Finished dev [unoptimized + debuginfo] target(s) in 1.28s
     Running `/tmp/nginx-logs/rust/target/debug/nginx_logs`
Problem parsing arguments: No pathname provided

usage: cargo run pathname

Export Nginx logs to a csv file.

positional arguments:
  pathname    path to a folder with the log files or to an specific file
```

Por último, creamos el ejecutable de este programa, como hemos explicado anteriormente:

```bash
cargo build --release
```

## Recursos

Programa para generar logs:

<https://github.com/CarlosAMolina/nginx-logs-generator>

Programa para convertir logs a csv:

<https://github.com/CarlosAMolina/nginx-logs>

## Links de este tutorial

- [Página principal](introduction.html)
