# Comparar tiempo de ejecución

## Introducción

En este apartado veremos el tiempo que requiere cada programa para procesar los logs creados anteriormente.

## Consideraciones iniciales

Empezamos comentando algunos puntos que se tuvieron en cuenta al desarrollar el programa, para que realizara sus funciones lo mas rápido posible.

En el caso de Rust, algunas consideraciones fueron:

- Al escribir los resultados en un archivo, para nuestro caso ayuda utilizar el método `BufWriter` ya que, como indica [su documentación](https://doc.rust-lang.org/std/io/struct.BufWriter.html), puede mejorar la velocidad en programas que realizan pequeñas y repetidas llamadas de escritura al mismo archivo.
- Si utilizamos expresiones regulares, hay que evitar perder tiempo por compilar varias veces la misma expresión regular, para ello [la documentación](https://docs.rs/regex/1.5.4/regex/index.html#example-avoid-compiling-the-same-regex-in-a-loop) recomienda utilizar el crate `lazy_loading`.

Respecto a Python, para evitar el incremento de tiempo por repetir compilar la expresión regular, se utiliza la función [re.compile](https://docs.python.org/3/library/re.html#re.compile).

Tanto en Rust como Python, obtener las partes que componen un log puede hacerse de diferentes formas y algunas son más rápidas que otras, las analizamos en la siguiente sección.

### Obtener partes del log

Al haber diferentes modos de parsear logs, es necesario buscar la manera que necesite menor tiempo. Para ello, en mi cuenta de GitHub he creado unas pruebas, en [Rust](https://github.com/CarlosAMolina/rust/blob/master/regex/performance-logs/src/main.rs) y [Python](https://github.com/CarlosAMolina/python/blob/master/regex/performance-logs/src/main.py), en las que obtengo los valores de parser un log 5.000 veces utilizando:

- Expresiones regulares: comparando diferentes funciones como `find`, `match`, `captures`, etc.
- Sin utilizar expresiones regulares, se buscan los caracteres que indican el fin de cada componente del log (ip remota, usuario remoto, hora, etc.) y se tiene en cuenta el número de caracteres hasta el siguiente elemento.

Para poder utilizar estos proyectos, los pasos son:

```bash
cd ~/Software
git clone git@github.com:CarlosAMolina/rust
git clone git@github.com:CarlosAMolina/python
```

Los resultados con Rust son:

```bash
$ cd ~/Software/rust/regex/performance-logs/
$ cargo build --release
$ ./target/release/performance
Time elapsed with match: 1.887184ms
Time elapsed with find: 6.531472ms
Time elapsed with captures: 32.598417ms
Time elapsed with no regex: 1.179403ms
Time elapsed with no regex one loop: 1.219159ms
```

Para cada resultado, se ha utilizado:

- Resultado `match`, el método empleado es [is_match](https://docs.rs/regex/latest/regex/struct.Regex.html#method.is_match), no sirve para obtener los valores que cumplan la expresión regular, pero sí para saber si la expresión regular tiene resultados o no.
- Resultado `find`, utiliza el método [find](https://docs.rs/regex/latest/regex/struct.Regex.html#method.find) que devuelve la posición de inicio y fin del primer resultado (el de más a la izquierda) en el string. Por lo que se van buscando los elementos del log teniendo en cuenta la posición del anterior encontrado. Es el equivalente a la función `search` de Python.
- Resultado `captures`, con el método [captures](https://docs.rs/regex/latest/regex/struct.Regex.html#method.captures) obtenemos todos los elementos con una sola expresión regular, guardados en grupos.
- Resultado `with no regex`, no hace uso de expresiones regulares, recorre el string en busca de la posición de los caracteres que indican el fin de cada elemento del log y suma el número de posiciones hasta el siguiente.
- Resultado `with no regex one loop`, igual que `with no regex` pero guarda los caracteres a buscar en un array que recorre con un loop.

El resultado que consume menos tiempo es no utilizar expresiones regulares, sin estar los caracteres a buscar en un array.

Con Python, tenemos:

```bash
$ cd ~/Software/python/regex/performance-logs/
$ python src/main.py
Time elapsed match: 48.98829100011426ms
Time elapsed search: 49.03245400009837ms
Time elapsed match groups: 48.159387999930914ms
Time elapsed search groups: 48.585519999960525ms
Time elapsed without regex: 50.20641400005843ms
```

Para estos resultados se ha utilizado:

- Resultado `match`, utiliza la función [re.match](https://docs.python.org/3/library/re.html#re.match) que solo busca si la expresión regular se cumple al inicio del string analizado, por lo que cada vez que se detecta un elemento del log, para buscar el siguiente se analiza el string desde la última posición del elemento encontrado mas el número de caracteres hasta el siguiente.
- Resultado `search`, emplea la función [re.search](https://docs.python.org/3/library/re.html#re.search) que busca la primera coincidencia (la que hay más a la izquierda del string) de la expresión regular en cualquier posición del string; el modo de encontrar cada elemento ha sido igual que con `match`.
- Resultado `match groups`, la función utilizada es [re.match](https://docs.python.org/3/library/re.html#re.match) pero se le pasa una expresión regular que busca todos los elementos a la vez, cada uno guardado en un grupo.
- Resultado `search groups`, igual que `match groups` pero la función empleada es [re.search](https://docs.python.org/3/library/re.html#re.search).
- Resultado `without regex`: se buscan elementos que determinan el fin de cada parte del log y se tiene en cuenta el número de caracteres hasta el siguiente.

En el caso de Python, los mejores resultados se tienen con la opción `match` de las expresiones regulares utilizando una expresión regular que capture todos los elementos de una vez.

¡Ya tenemos la manear de parser logs en cada lenguaje!

## Rust

Al obtener los resultados con Rust, lo haremos para la opción más rápida, la cual no utiliza expresiones regulares, y también para la opción más rápida y lenta con expresiones regulares, de modo que podamos comparar las mediciones con Python, donde la opción que requiere menos tiempo sí que emplea expresiones regulares.

### Opción mas rápida

Sin tener ningún programa ejecutándose en el ordenador, lanzamos nuestro parseador de logs:

```bash
$ cd ~/Software/nginx-logs/rust/
$ ./target/release/nginx_logs ~/Software/poc-rust/logs/
Checking: /home/x/Software/poc-rust/logs/
File with logs as csv: /home/x/Software/poc-rust/logs/result.csv
File with not parsed logs: /home/x/Software/poc-rust/logs/error.txt
Init file: /home/x/Software/poc-rust/logs/access.log.9.gz
Init file: /home/x/Software/poc-rust/logs/access.log.8.gz
Init file: /home/x/Software/poc-rust/logs/access.log.7.gz
Init file: /home/x/Software/poc-rust/logs/access.log.6.gz
Init file: /home/x/Software/poc-rust/logs/access.log.5.gz
Init file: /home/x/Software/poc-rust/logs/access.log.4.gz
Init file: /home/x/Software/poc-rust/logs/access.log.3.gz
Init file: /home/x/Software/poc-rust/logs/access.log.2.gz
Init file: /home/x/Software/poc-rust/logs/access.log.1
Init file: /home/x/Software/poc-rust/logs/access.log
Time elapsed: 720.718476ms
```

El archivo `result.csv` generado ocupa 103M, y el archivo `error.txt` con logs no parseados está vacío por lo que todos han sido procesados correctamente.

Ejecutaremos el programa varias veces, borrando antes de cada proceso los archivos de resultados creados para que la escritura de nuevos archivos no se vea afectada por algunos ya existentes:

```bash
rm ~/Software/poc-rust/logs/error.txt ~/Software/poc-rust/logs/result.csv
```

Veremos el resumen del tiempo requerido en cada ejecución más adelante.

### Opciones con expresiones regulares

Para trabajar con expresiones regulares, debemos cambiar algunos archivos.

Primero, modificamos el archivo `Cargo.toml`, dentro del apartado `[dependencies]`, descomentamos:

```bash
lazy_static = "1.4.0"
regex = "1.5.6"
```

En el archivo `src/m_log.rs`, descomentamos:

```bash
use lazy_static::lazy_static;
use regex::Regex;
```

También, en este archivo comentamos la función `get_log` utilizada actualmente y descomentamos la función `get_log` que emplea expresiones regulares, tenemos dos opciones, una con el método `find` y la otra con `captures`. Recordemos que, de utilizar expresiones regulares, entre los métodos que nos da cada parte de log, el método `find` era la opción más rápida en Rust y el método `captures` el más lento, pero aun así mejores que en Python cuando comparamos expresiones regulares al inicio de este apartado.

Para cada método, compilamos el programa y repetimos las mediciones como hicimos antes. Los valores de las mediciones se mostrarán en una tabla resumen más adelante.

## Python

Al igual que con Rust, lanzamos nuestro parseador sin tener ningún otro programa ejecutándose en el ordenador:

```bash
$ cd ~/Software/nginx-logs/python/
$ python src/main.py ~/Software/poc-rust/logs
Checking: /home/x/Software/poc-rust/logs
File with logs as csv: /home/x/Software/poc-rust/logs/result.csv
File with not parsed logs: /home/x/Software/poc-rust/logs/error.txt
Init file: /home/x/Software/poc-rust/logs/access.log.9.gz
Init file: /home/x/Software/poc-rust/logs/access.log.8.gz
Init file: /home/x/Software/poc-rust/logs/access.log.7.gz
Init file: /home/x/Software/poc-rust/logs/access.log.6.gz
Init file: /home/x/Software/poc-rust/logs/access.log.5.gz
Init file: /home/x/Software/poc-rust/logs/access.log.4.gz
Init file: /home/x/Software/poc-rust/logs/access.log.3.gz
Init file: /home/x/Software/poc-rust/logs/access.log.2.gz
Init file: /home/x/Software/poc-rust/logs/access.log.1
Init file: /home/x/Software/poc-rust/logs/access.log
Time elapsed: 9.791666581000072s
```

Eliminamos archivos generados para que no afecten a próximas ejecuciones y repetimos las medidas tres veces mas:

```bash
rm ~/Software/poc-rust/logs/error.txt ~/Software/poc-rust/logs/result.csv
rm -rf src/__pycache__
```

Los resultados los comentamos a continuación.

## Representación gráfica de las mediciones

La representación se realiza con el proyecto `nginx-logs`, el cual tiene unos scripts en Python para esta función.

En el archivo `~/Software/nginx-logs/measure/measure/results/execution-time.csv` están registradas las medidas conseguidas hasta ahora, pasamos a representarlas gráficamente.

La ruta con la que trabajar es:

```bash
cd ~/Software/nginx-logs/measure/plot/
```

Al ser un script en Python que utiliza librerías como `matplotlib`, instalamos los requisitos:

```bash
python -m venv ~/Software/nginx-logs/env
source ~/Software/nginx-logs/env/bin/activate
pip install -r requirements.txt
```

Ya podemos crear las gráficas:

```bash
python src/plot_results.py time
```

Cuando finalice, tendremos archivos `.png` con las gráficas en la ruta ` ~/Software/nginx-logs/measure/plot/src/results/`.

## Resultados

Pasamos a comentar las medidas obtenidas en este apartado.

### Tiempos de ejecución

Las mediciones de este apartado, y su valor medio, han sido:

Descripción                                            | Ejecución 1 | Ejecución 2 | Ejecución 3 | Ejecución 4 | Media
-------------------------------------------------------|-------------|-------------|-------------|-------------|---------
Rust opción más rápida (búsqueda por índice, no regex) | 0.721s      | 0.579s      | 0.577s      | 0.575s      | 0.613
Python opción más rápida (regex match, una sola regex) | 9.792s      | 9.736s      | 9.728s      | 9.682s      | 9.734
Rust regex más rápida (regex find e índices)           | 1.413s      | 1.413s      | 1.414s      | 1.409s      | 1.412
Rust regex más lenta (regex captures, una sola regex)  | 12.213s     | 12.119s     | 12.147s     | 11.998s     | 12.119

Si lo representamos en una gráfica:

![](execution-time.png)

> Media tiempo de ejecución

Hemos visto que Rust es mucho mas rápido que Python, necesitando 0.613s el primer lenguaje y 9.734s Python, como puede verse en las dos primeras columnas de esta gráfica:

Para Rust, el mejor tiempo se obtiene sin utilizar expresiones regulares, se buscan caracteres que indican el fin de cada elemento del log; en cambio, con Python el modo empleado es la función `match` con una sola expresión regular que detecta todas las partes del log.

En la imagen anterior, se han añadido las dos últimas columnas para conocer qué tiempo necesita el programa en Rust utilizando expresiones regulares, comparando la expresión regular más rápida y la más lenta que, como vemos, provoca que tarde más que Python, lo comentamos a continuación.

### Python más rápido que Rust

Como vimos al inicio de este apartado, en Rust se tienen mejores tiempos de no utilizar expresiones regulares, pero como curiosidad, si el programa las utilizara, puede llegar a tardar más tiempo que Python.

Es verdad que, cuando estudiamos el modo más rápido de parsear logs, Rust era más rápido que Python con expresiones regulares, pero porque analizamos el mismo log (aunque se analizó una gran cantidad de veces), de trabajar con los archivos de logs anteriores, hemos visto que, con el método `captures` se tiene un programa más lento que su versión en Python.

Puede leerse más sobre esta pérdida de velocidad en Rust respecto a Python en este hilo de [Reddit](https://www.reddit.com/r/rust/comments/5zit0e/regex_captures_slow_compared_to_python/).

Vemos que, con expresiones regulares, Rust puede hacer el análisis en 1.412s, el cual es mejor que Python, pero de utilizar el método de la expresión regular que da los resultados más lentos, se tiene un programa de menor velocidad que en Python, requiriendo 12.119s.

### Archivo csv generado

El tamaño del archivo `result.csv` creado es de 103M tanto en Rust (con todos sus métodos) como en Python.

Todos los archivos de resultados tienen el mismo contenido. Entre el generado por Rust y Python, la única diferencia es el salto de línea empleado en cada archivo, puede verse con el programa [meld](https://meldmerge.org/) ejecutando el siguiente comando (se ha cambiado el nombre de los archivos de resultados y movido a la carpeta `results`):

```bash
$ meld ~/Software/poc-rust/logs/results/result-python.csv ~/Software/poc-rust/logs/results/result-rust-by-index.csv
```

![](results-file-difference.png)

> Diferencia entre archivo csv generado por Rust y Python

## Links de este tutorial

- [Siguiente apartado. Comparar memoria](09-compare-memory.html)
- [Página principal](introduction.html)

