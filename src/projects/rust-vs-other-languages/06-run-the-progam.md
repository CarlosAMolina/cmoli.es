Primero, debemos obtener logs que analizar. Utilizaremos el programa descargado previamente al preparar los proyectos.

Crearemos en la ruta `~/Software/poc-rust/logs/` los siguiente archivos de logs:

- access.log.2.gz, 110 MiB (1.4 GiB sin comprimir).
- access.log.1, 477 MiB.
- access.log, 954 MiB.

Para ello, con el siguiente comando, indicamos la ruta de destino (el programa creará la carpeta llamada `logs`), y el tamaño de los archivos (en Gigabytes):

```bash
cargo run ~/Software/poc-rust 1.5 0.5 1
```
