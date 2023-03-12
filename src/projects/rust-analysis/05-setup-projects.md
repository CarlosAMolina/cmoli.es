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

## Recursos

Programa para generar logs:

<https://github.com/CarlosAMolina/nginx-logs-generator>

## Links de este tutorial

- [Página principal](introduction.html)

