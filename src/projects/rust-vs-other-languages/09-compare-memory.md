# Comparar memoria

## Introducción

Pasamos a medir el uso de memoria por parte del programa al convertir los archivos de logs a csv.

Para ello, primero es necesario encontrar una herramienta capaz de medir la memoria.

## Herramienta elegida

A la hora de seleccionar el software con el que medir la memoria utilizada por nuestro programa, hay que tener en cuenta que estamos ante un programa por línea de comandos que se ejecuta en nuestro propio equipo; esta característica descarta, por ejemplo, programas que realicen pruebas de estrés enviando peticiones en lugar de lanzar el programa a analizar.

Lo primero que probé fue trabajar con los comandos `top` y `htop`, pero no fueron opciones válidas ya que, al medir el ejecutable de Rust (puede filtrarse el proceso por el nombre `nginx_logs`), se muestra un uso de 0% de memoria. En el caso de Python (filtramos el proceso por el nombre `python`), si se mostraría valores para la memoria utilizada, pero viendo que con Rust no es una opción válida, es mejor buscar otra alternativa.

Tampoco es recomendable usar el comando `ps` para medir la memoria. Puede verse [en este link](https://stackoverflow.com/questions/131303/how-can-i-measure-the-actual-memory-usage-of-an-application-or-process), que, entre otros aspectos, indica la cantidad de memoria reservada, no la cantidad real utilizada.

Finalmente utilicé [Valgrind](https://valgrind.org/docs/manual/ms-manual.html) para realizar estas tres mediciones:

- Opción heap: mide la memoria reservada con funciones como malloc, calloc, realloc, memalign, new, new[] y similares, pero no por llamadas del sistema de bajo nivel como mmap, mremap y brk.
- Opción heap y stack: mide la memoria heap y stack.
- Opción pages as heap (lo llamo `page level`): para medir memoria heap, memoria stack, llamadas del sistema de bajo nivel, tamaño del código, datos y segmentos BSS. Esto es lo que suelen medir herramientas como top.

## Instalación Valgrind

TODO

## Ejecutar medición

TODO

## Resultados

He tenido que medir menos archivos con respecto al inicio de este tutorial para reducir un poco el tiempo de medición y evitar un mensaje de warning que mostraba Valgrind con respecto a la configuración de medición. Los archivos analizados ocupan 25 MB (al descomprimirlos ocupan 109 MB), han sido los siguientes:

```bash
12M access.log
7.5M access.log.1
612K access.log.2.gz
824K access.log.3.gz
1,1M access.log.4.gz
700K access.log.5.gz
776K access.log.6.gz
496K access.log.7.gz
700K access.log.8.gz
776K access.log.9.gz
```

Indicar que:

- El programa desarrollado analiza los archivos en orden de mayor número a menor, es decir, empieza por `access.log.9.gz`, luego `access.log.8.gz` y por último `access.log.1` y `access.log`.
- Cuando se mide con Valgrind, el programa tarda más, por lo que el eje horizontal de tiempo no representa lo que tardaría el programa en realidad.

Los resultados han sido los siguientes.

- Heap
  - Rust necesita cerca de 100 kB la mayor parte del tiempo y luego baja a cerca de 26 kB. La parte de los 100 kB corresponde al análisis de los archivos comprimidos en `gz` y la bajada se produce porque ya no descomprime archivos (analiza `access.log.1` y `access.log`).
  - Python está en el orden de MB, se mantiene cerca de 2 MB al analizar archivos comprimidos en `.gz` y luego presenta picos al analizar archivos de logs que no están comprimidos, siendo el pico más alto de casi 26 MB.

![](metrics-memory-massif-rust-heap-only.png)

> Memoria heap Rust

![](metrics-memory-massif-python-heap-only.png)

> Memoria heap Python

- Heap y stack

  - Rust y Python: comportamiento similar que al medir solo `heap` (presenta la misma gráfica) aunque con unos valores de unos pocos kB más.

- Heap y stack

![](metrics-memory-massif-rust-add_stacks.png)

> Memoria heap y stack Rust

![](metrics-memory-massif-python-add_stacks.png)

> Memoria heap y stack Python

- Page level
  - Rust: los valores aumentan a cerca de 5 MB, presenta un comportamiento casi constante.
  - Python: la mayor parte del tiempo está entre 22 MB y 30 MB hasta que se producen los picos comentados antes por analizar los dos archivos no comprimidos, siendo el mayor pico de 52 MB.

![](metrics-memory-massif-rust-add-pages-as-heap.png)

> Memoria page level Rust

![](metrics-memory-massif-python-add-pages-as-heap.png)

> Memoria page level Python

Se observa que el consumo de memoria es mayor al descomprimir que al leer los archivos descomprimidos; aunque esto depende del lenguaje, Rust consume más memoria al descomprimir y Python al leer archivos no comprimidos; será por cómo están implementadas las librerías que he utilizado o cómo he creado yo el código.

