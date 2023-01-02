# Código Rust vs Python

## Introducción 

Iniciamos con esta entrada las comparaciones entre Rust y Python. 

Observaremos partes del código para mostrar las similitudes y diferencias en el programa desarrollado en estos dos lenguajes.

## Partes del programa

El programa escrito en Rust y Python está organizado en módulos de manera que sea sencillo comparar ambos lenguajes.

### Recibir los valores dados por el usuario

Lo primero que necesita realizar el programa es recibir por línea de comandos los valores dados por el usuario.

### Ordenar archivos de logs a analizar

Una vez se conoce la ruta con los archivos a analizar, deben ordenarse desde el más antiguo hasta el más actual. Esto es necesario para que el archivo `csv` final tenga los logs ordenados cronológicamente.

### Modificar logs

Al leer los logs, debe separarse con comas cada parte (dirección IP, paths solcitidados, códigos de respuesta, etc) para generar el archivo .csv final.

## Conclusión

Con lo visto en los ejemplos anteriores, extraemos las siguientes conclusiones:

- El código en Python es más sencillo que Rust.

## Recursos

Programa que convierte archivos de logs en `csv`:

<https://github.com/CarlosAMolina/nginx-logs>

- [Página principal](introduction.html).

