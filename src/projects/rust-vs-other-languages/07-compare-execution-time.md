# Comparar tiempo de ejecución

## Introducción

En este apartado veremos el tiempo que requiere cada programa para procesar los logs creados en el apartado anterior.

## Consideraciones iniciales

Al haber diferentes modos de parsear logs, es necesario buscar la opción más óptima. Para ello, en mi cuenta de GitHub he creado unas pruebas en las que obtengo los valores de un log utilizando:

- Expresiones regulares: comparando diferentes opciones que proporcionan para encontrar los resultados.
- Sin utilizar expresiones regulares, se buscan los caracteres que indican el fin de cada componente del log (ip remota, usuario remoto, hora, etc...) y se tiene en cuenta el número de caracteres hasta el siguiente elemento.

Para poder utilizar estos proyectos, los pasos son:

```bash
cd ~/Software
git clone git@github.com:CarlosAMolina/python
git clone git@github.com:CarlosAMolina/rust
```

Los resultados con Python son:

```bash
$ cd ~/Software/python/regex/performance-logs/
$ python src/main.py
Time elapsed match: 51.8112699996891ms
Time elapsed search: 51.94285400011722ms
Time elapsed match groups: 51.19512799956283ms
Time elapsed search groups: 51.559934000124485ms
Time elapsed without regex: 70.69803299964406ms
```

Los cuatro primeros resultados son con expresiones regulares y el último sin ellas.

Para Rust, tenemos:

```bash
$ cd ~/Software/rust/regex/performance-logs/
$ cargo build --release
$ ./target/release/performance
Time elapsed with match: 1.878929ms
Time elapsed with find: 8.992845ms
Time elapsed with captures: 36.62146ms
Time elapsed with no regex: 1.174077ms
Time elapsed with no regex one loop: 1.206302ms
```

Los primeros tres resultados utilizan expresiones regulares, y los dos últimos no. La diferencia entre el penúltimo y último resultado es que el último tiene los caracteres a buscar en un array y se recorren en un loop, mientras que el penúltimo trabaja con cada uno por separado, también cambia un poco cómo se calcula la última posición.

En el caso de Python, los mejores resultados se tienen con la opción `match` de las expresiones regulares, mientras que en Rust es mejor no utilizar expresiones regulares.

## Rust

Sin tener ningún programa ejecutándose en el ordenador, lanzamos nuestro parseador de logs:

```bash
$ cd ~/Software/nginx-logs/rust/
$ ./target/release/nginx_logs ~/Software/poc-rust/logs/
Checking: /home/x/Software/poc-rust/logs/
File with logs as csv: /home/x/Software/poc-rust/logs/result.csv
File with not parsed logs: /home/x/Software/poc-rust/logs/error.txt
Init file: /home/x/Software/poc-rust/logs/access.log.2.gz
Init file: /home/x/Software/poc-rust/logs/access.log.1
Init file: /home/x/Software/poc-rust/logs/access.log
Time elapsed: 29.436084606s
```

El archivo `result.csv` generado ocupa 2.7G, y el archivo `error.txt` con logs no parseados está vacío por lo que todos los han sido procesados correctamente.

Ejecutaremos el programa varias veces; para que resultados anteriores no interfieran, borramos los archivos de resultados creados:

```bash
rm error.txt result.csv
```

De este modo en todas las ejecuciones se creará un archivo nuevo en lugar de detectar que ya existe.

Volvemos a repetir los comandos anteriores; los tiempos de ejecución han sido:

- Ejecución 1: 29.436084606s
- Ejecución 2: 30.226746264s
- Ejecución 3: 33.715843557s
- Ejecución 4: 30.339168491s

Como vemos, los tiempos de ejecución son de media: 30.929460729499997s.

En todas las ejecuciones, el archivo `result.csv` es idéntico, todos tienen el mismo hash.

## Python

Al igual que con Rust, lanzamos nuestro parseador sin tener ningún otro programa ejecutándose en el ordenador:

```bash
$ cd ~/Software/nginx-logs/rust/
Checking: /home/x/Software/poc-rust/logs/
File with logs as csv: /home/x/Software/poc-rust/logs/result.csv
File with not parsed logs: /home/x/Software/poc-rust/logs/error.txt
Init file: /home/x/Software/poc-rust/logs/access.log.2.gz
Init file: /home/x/Software/poc-rust/logs/access.log.1
Init file: /home/x/Software/poc-rust/logs/access.log
Time elapsed: 271.78013042500015s
```

Eliminamos archivos generados para que no afecten a próximas ejecuciones y repetimos las medidas 4 veces mas:

```bash
rm error.txt result.csv
rm -rf src/__pycache__
```

Los resultados fueron:

- Ejecución 1: 271.78013042500015s
- Ejecución 2: 275.31400713799985s
- Ejecución 3: 274.71298764999983s
- Ejecución 4: 277.1358656340003s

La media con Python es de 274.73574771175004s

Como era de esperar, todos los logs han sido parseados correctamente y los archivos `.csv` generados son iguales, tienen el mismo hash (el hash del archivo generado pro Python y Rust sí es distinto).


## Comentario de los resultados

El tamaño del archivo `result.csv` generado es de 2.7G tanto en Rust como en Python.

Rus es mucho mas rápido que Python, 30.930s vs 274.736s (4min y 36.736s).

### Python más rápido que Rust

Como comentamos al inicio de este apartado, en Rust se tienen mejores tiempos de no utilizar expresiones regulares, pero como curiosidad, si el programa las utilizara, tardaría más tiempo que Python.

Al inicio de este apartado Rust era más rápido que Python con expresiones regulares pero porque solo analizamos un log, de trabajar con los archivos anteriores, se pasaría de TODO a TODO, lo que da como resultado un peor programa que su versión en Python.

Para ver esto, debemos cambiar los siguientes archivos del programa en Rust:

TODO

