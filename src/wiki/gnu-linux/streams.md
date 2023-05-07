# Streams

## ¿Qué son?

Son canales de comunicación de entrada y salida, entre un programa y su entorno.

Los streams se representan como `file descriptors`.

Los 3 streams estándar son:

Standard stream | Nombre          | File descriptor
---------------------------------------------------
stdin           | Standard Input  | 0
stdout          | Standard Output | 1
stderr          | Standard Error  | 2

## Redirección

Ejemplo redirigir errores a un archivo:

```bash
./program 2> errors.txt
```

## Recursos

<https://www.putorius.net/linux-io-file-descriptors-and-redirection.html>

