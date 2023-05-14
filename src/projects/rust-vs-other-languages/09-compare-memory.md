# Comparar memoria

## Contenidos

- [Introducción](#introducción)
- [Herramienta elegida](#herramienta-elegida)
- [Instalación Valgrind](#instalación-valgrind)
- [Ejecutar medición](#ejecutar-medición)
- [Representación gráfica de las mediciones](#representación-gráfica-de-las-mediciones)
- [Resultados](#resultados)
- [Recursos](#recursos)
- [Links de este tutorial](#links-de-este-tutorial)

## Introducción

Pasamos a medir el uso de memoria por parte del programa al convertir los archivos de logs a csv.

Para ello, primero es necesario encontrar una herramienta capaz de medir la memoria.

## Herramienta elegida

A la hora de seleccionar el software con el que medir la memoria utilizada por nuestro programa, hay que tener en cuenta que estamos ante un programa por línea de comandos que se ejecuta en nuestro propio equipo; esta característica descarta, por ejemplo, herramientas que realicen pruebas de estrés enviando peticiones en lugar de lanzar el programa a analizar.

Lo primero que probé fue a trabajar con los comandos `top` y `htop`, pero no fueron opciones válidas ya que, al medir el ejecutable de Rust (puede filtrarse el proceso por el nombre `nginx_logs`), se muestra un uso de 0% de memoria. En el caso de Python (filtramos el proceso por el nombre `python`), sí se muestran valores para la memoria utilizada, pero viendo que con Rust no es una opción válida, es mejor buscar otra alternativa.

Tampoco es recomendable usar el comando `ps` para medir la memoria. Puede verse [en este link](https://stackoverflow.com/questions/131303/how-can-i-measure-the-actual-memory-usage-of-an-application-or-process), que, entre otros aspectos, indica la cantidad de memoria reservada, no la cantidad real utilizada.

Finalmente, utilicé [Valgrind](https://valgrind.org/docs/manual/ms-manual.html), con su opción [Massif](https://valgrind.org/docs/manual/ms-manual.html) para realizar estas tres mediciones:

- Heap: mide la memoria reservada con funciones como malloc, calloc, realloc, memalign, new, new[] y similares, pero no por llamadas del sistema de bajo nivel como mmap, mremap y brk.
- Heap y stack: mide la memoria heap y stack.
- Page level: para medir toda la memoria utilizada por el programa (memoria heap, memoria stack, llamadas del sistema de bajo nivel, tamaño del código, datos y segmentos BSS). Esto es lo que suelen medir herramientas como top.

Massif, a demás de poder dar estas mediciones, también permite conocer qué partes del programa trabajan con la memoria.

## Instalación Valgrind

Si es posible instalar Valgrind desde los repositorios de nuestro sistema operativo, es la manera más sencilla. Por ejemplo, en Arch Linux solo habría que ejecutar:

```bash
sudo pacman -S valgrind
```

De no estar disponible en los repositorios o de querer una versión distinta, puede descargarse su código en este [link](https://valgrind.org/downloads/) y las instrucciones vienen explicadas en el archivo README.

Para verificar la versión instalada:

```bash
$ valgrind --version
valgrind-3.20.0
```

Respecto a visualizar los resultados de manera gráfica, utilizaremos unos scripts propios, aunque también existe el programa [massif-visualizer](https://apps.kde.org/es/massif-visualizer/). Si quisiéramos instalar `massif-visualizer`, puede utilizarse el enlace anterior o los repositorios oficiales de nuestra distribución, ejemplo en Arch Linux:

```bash
sudo pacman -S massif-visualizer
```

## Ejecutar medición

En el proyecto nginx-logs que descargamos previamente, tenemos un [script](https://github.com/CarlosAMolina/nginx-logs/blob/main/measure/measure/run-and-measure-memory) que se encarga de realizar las mediciones con Valgrind automáticamente.

Este script realizará tres ejecuciones del programa en Rust y otras tres en Python, estando estas ejecuciones analizadas con Valgrind, y guardará los archivos con las mediciones; también realiza acciones como eliminar los archivos creados por el programa para que cada ejecución no se vea afectada por la anterior.

Utilizamos Valgrind con su opción Massif y elegimos como unidad de tiempo milisegundos. Por defecto, la unidad de tiempo en Massif son las instrucciones ejecutadas, como puede verse en su documentación, pero hemos cambiado esto; otra opción disponible para la unidad de tiempo es usar el número de bytes reservados y liberados en la heap y stack.

Primero, los logs a analizar hemos de copiarlos en `/tmp/logs`, que es la ruta que el script mandará que analice Valgrind:

```bash
cp -r ~/Software/poc-rust/logs /tmp/
```

Procedemos con las mediciones, para no afectar a los resultados, he cerrado el resto de programas que tenía ejecutándose:

```bash
cd ~/Software/nginx-logs/measure/measure
./run-and-measure-memory
```

Los archivos de resultados se guardarán en la carpeta `~/Software/nginx-logs/measure/measure/results/`.

Hay que tener en cuenta que, al utilizar Valgrind, la ejecución del programa necesita más tiempo. Por ejemplo, el caso que más tiempo requiere es medir la versión Python analizando el uso de memoria heap y stack, necesitando sobre 1h y 30min.

## Representación gráfica de las mediciones

Ahora queda representar gráficamente los archivos que hemos creado en `~/Software/nginx-logs/measure/measure/results/`.

Pueden utilizarse las mediciones que obtuve, las adjunté al proyecto `nginx-logs` que hemos ido utilizando:

```bash
cd ~/Software/nginx-logs/measure/measure/results
tar xvf valgrind-measure-python-3-11.tar.gz
mv valgrind-measure-python-3-11/* .
```

Si quisiéramos ver gráficamente las mediciones que se han guardado en un archivo, la manera más sencilla es utilizar `massif-visualizer`, por ejemplo:

```bash
massif-visualizer results/massif.out.measure-1.rust.heap-only
```

Esta herramienta no es solamente la manera más rápida de representar los resultados, sino que permite analizarlos observando qué partes del código han gestionado la memoria.

En lugar de utilizar `massif-visualizer`, al igual que hicimos al representar las mediciones del tiempo de ejecución, trabajaremos con los scripts disponibles en el proyecto `nginx-logs`, ya que permiten mayor personalización. Cambiamos nuestro directorio de trabajo:

```bash
cd ~/Software/nginx-logs/measure/plot/
```

Activamos el entrono virtual que creamos anteriormente al analizar el tiempo de ejecución, y que tiene instaladas las librerías externas necesarias:

```bash
source ~/Software/nginx-logs/env/bin/activate
```

Generamos las gráficas con:

```bash
python src/plot_results.py memory
```

En la ruta ` ~/Software/nginx-logs/measure/plot/src/results/` tendremos las gráficas en formato `.png`.

## Resultados

Los resultados del uso de memoria han sido los siguientes.

- Heap
  - Rust necesita cerca de 100 kB la mayor parte del tiempo y al final baja su consumo sobre 26 kB. La parte de los 100 kB corresponde al análisis de los archivos comprimidos en `gz` y la bajada se produce porque ya no descomprime archivos (analiza `access.log.1` y `access.log`).
  - Python está en el orden de MB, se mantiene cerca de 2 MB al analizar archivos comprimidos en `.gz` y luego presenta picos al analizar archivos de logs que no están comprimidos, siendo el pico más alto de poco más de 26 MB.

![](metrics-memory-massif-rust-heap-only.png)

> Memoria heap Rust

![](metrics-memory-massif-python-heap-only.png)

> Memoria heap Python

- Heap y stack
  - Tanto en Rust y Python, el comportamiento es similar que al medir solo `heap` (presenta la misma gráfica) aunque con unos valores de unos pocos kB más.

![](metrics-memory-massif-rust-add_stacks.png)

> Memoria heap y stack Rust

![](metrics-memory-massif-python-add_stacks.png)

> Memoria heap y stack Python

- Page level
  - En Rust, los valores aumentan a cerca de 5.2 MB, presenta un comportamiento casi constante.
  - Sobre Python, la mayor parte del tiempo está entre 22 MB y 30 MB hasta que se producen los picos comentados antes por analizar los dos archivos no comprimidos, siendo el mayor pico de 51.5 MB.

![](metrics-memory-massif-rust-add-pages-as-heap.png)

> Memoria page level Rust

![](metrics-memory-massif-python-add-pages-as-heap.png)

> Memoria page level Python

Como comentarios finales de estos resultados, Rust presenta un menor consumo que Python.

También, hay diferencias entre estos lenguajes al analizar la memoria heap y stack. Rust tiene mayor consumo al analizar archivos que debe descomprimir, que al trabajar con aquellos que no están comprimidos; pero en el caso de Python, los picos de memoria se producen al trabajar con los archivo no comprimidos.

Como se aprecia en las gráficas, el eje temporal es mayor al que obtuvimos al comparar el tiempo de ejecución. Esto se debe a que el uso de Valgrind incrementa el tiempo del programa; es decir, el eje temporal conseguido en este apartado no representa lo que tardaría el programa en realidad.

## Recursos

Comando `ps` no es recomendable para medir memoria:

<https://stackoverflow.com/questions/131303/how-can-i-measure-the-actual-memory-usage-of-an-application-or-process>

Massif documentación:

<https://valgrind.org/docs/manual/ms-manual.html>

Massif Visualizer:

<https://apps.kde.org/es/massif-visualizer/>

Script en proyecto nginx-logs para medir memoria:

<https://github.com/CarlosAMolina/nginx-logs/blob/main/measure/measure/run-and-measure-memory>

Valgrind descarga:

<https://valgrind.org/downloads/>

Valgrind documentación:

<https://valgrind.org/docs/manual/ms-manual.html>

## Links de este tutorial

- [Siguiente apartado. Comparar CPU](10-compare-cpu.html)
- [Página principal](introduction.html)

