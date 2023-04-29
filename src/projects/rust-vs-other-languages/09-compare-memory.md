Para medir la memoria, no puede utilzarse los comandos `top` y `htop`, ya que para el binario de Rust, el proceso muestra 0% de memoria. (TODO verificar esto, a ver si aplica para top htop y también para ps, y ver si aplica también para python).

Tampoco es recomendable usar el comando `ps` para medir la memoria, puede verse [en este link](https://stackoverflow.com/questions/131303/how-can-i-measure-the-actual-memory-usage-of-an-application-or-process).

## Herramienta elegida

Finalmente utilicé Valgrind (https://valgrind.org/docs/manual/ms-manual.html), permite hacer estas 3 mediciones:

- Opción heap: mide la memoria reservada con funciones como malloc, calloc, realloc, memalign, new, new[] y similares, pero no por llamadas del sistema de bajo nivel como mmap, mremap y brk.
- Opción heap y stack: mide la memoria heap y stack.
- Opción pages as heap (lo llamo `page level`): para medir memoria heap, memoria stack, llamadas del sistema de bajo nivel, tamaño del código, datos y segmentos BSS. Esto es lo que suelen medir herramientas como top.

He utilizado Valgrind porque el código que desarrollé es una herramienta por línea de comandos y Valgrind se ajusta a la perfección.

## Resultados

Medir memoria. Resultados

He tenido que medir menos archivos con respecto al inciio de este tutorial para reducir un poco el tiempo de medición y evitar un mensaje de warning que mostraba Valgrind con respecto a la configuración de medición. Los archivos analizados ocupan 25 MB (al descomprimirlos ocupan 109 MB), han sido los siguientes:

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

