# Comparar tiempo de ejecución

## Introducción

En este apartado veremos el tiempo que requiere cada programa para procesar los logs creados anteriormente.

Recordemos que, el tamaño de los archivos con logs es:

- access.log.2.gz, 110 MiB (1.4 GiB sin comprimir).
- access.log.1, 477 MiB.
- access.log, 954 MiB.

## Consideraciones iniciales

Empezamos comentando algunos puntos que se tuvieron en cuenta al escribir el programa, para que realizara sus funciones lo mas rápido posible.

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
Time elapsed with match: 1.878929ms
Time elapsed with find: 8.992845ms
Time elapsed with captures: 36.62146ms
Time elapsed with no regex: 1.174077ms
Time elapsed with no regex one loop: 1.206302ms
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
Time elapsed match: 51.8112699996891ms
Time elapsed search: 51.94285400011722ms
Time elapsed match groups: 51.19512799956283ms
Time elapsed search groups: 51.559934000124485ms
Time elapsed without regex: 70.69803299964406ms
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

El archivo `result.csv` generado ocupa 2.7G, y el archivo `error.txt` con logs no parseados está vacío por lo que todos han sido procesados correctamente.

Ejecutaremos el programa varias veces; para que resultados anteriores no interfieran, borramos los archivos de resultados creados:

```bash
rm error.txt result.csv
```

De este modo, en todas las ejecuciones se creará un archivo nuevo sin tener en cuenta uno ya existe.

Volvemos a repetir los comandos anteriores; los tiempos de ejecución han sido:

Descripción                                            | Ejecución 1 | Ejecución 2 | Ejecución 3 | Ejecución 4 | Media
-------------------------------------------------------|-------------|-------------|-------------|-------------|--------
Rust opción más rápida (búsqueda por índice, no regex) | 29.436s     | 30.227s     | 33.716s     | 30.339s     | 30.929s

Como vemos, los tiempos de ejecución tienen de media: 30.929s.

En todas las ejecuciones, el archivo `result.csv` es idéntico, todos tienen el mismo hash.

## Python

Al igual que con Rust, lanzamos nuestro parseador sin tener ningún otro programa ejecutándose en el ordenador:

```bash
$ cd ~/Software/nginx-logs/python/
$ python src/main.py ~/Software/poc-rust/logs
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

Los resultados fueron (los añado en una nueva línea siguiendo la tabla anterior):

Descripción                                            | Ejecución 1 | Ejecución 2 | Ejecución 3 | Ejecución 4 | Media
-------------------------------------------------------|-------------|-------------|-------------|-------------|---------
Rust opción más rápida (búsqueda por índice, no regex) | 29.436s     | 30.227s     | 33.716s     | 30.339s     | 30.929s
Python opción más rápida (regex match, una sola regex) | 271.780s    | 275.314s    | 274.713s    | 277.136s    | 274.736s

Siendo la media con Python de 274.736s (4min y 36.736s).

Como era de esperar, todos los logs han sido parseados correctamente y los archivos `.csv` generados con Python son iguales, tienen el mismo hash (el hash del archivo generado pro Python y Rust sí es distinto).

## Comentario de los resultados

El tamaño del archivo `result.csv` generado es de 2.7G tanto en Rust como en Python.

Hemos visto que Rust es mucho mas rápido que Python, necesitando 30.930s el primer lenguaje y 274.736s (4min y 36.736s) Python, como puede verse en las dos primeras columnas de esta gráfica:

![](execution-time.png)

> Media tiempo de ejecución

Para Rust, el mejor tiempo se obtiene sin utilizar expresiones regulares, se buscan caracteres que indican el fin de cada elemento del log; en cambio, con Python el modo empleado es la función `match` con una sola expresión regular que detecta todas las partes del log.

En la imagen anterior, se han añadido las dos últimas columnas para conocer qué tiempo necesita el programa en Rust utilizando expresiones regulares, comparando la expresión regular más rápida y la más lenta que, como vemos, provoca que tarde más que Python, lo comentamos a continuación.

### Python más rápido que Rust

Como vimos al inicio de este apartado, en Rust se tienen mejores tiempos de no utilizar expresiones regulares, pero como curiosidad, si el programa las utilizara, puede llegar a tardar más tiempo que Python.

Es verdad que, al analizar la manera más rápida de parsear logs, Rust era más rápido que Python con expresiones regulares, pero porque solo analizamos un log, de trabajar con los archivos de logs anteriores, daría como resultado un peor programa que su versión en Python.

Para ver esto, debemos cambiar algunos archivos del programa en Rust.

Añadimos en el archivo `Cargo.toml`, dentro del apartado `[dependencies]`:

```bash
lazy_static = "1.4.0"
regex = "1.5.6"
```

En el archivo `src/m_log.rs`, descomentamos:

```bash
use lazy_static::lazy_static;
use regex::Regex;
```

Y comentamos la función `get_log` utilizada actualmente y descomentamos la función `get_log` que emplea expresiones regulares, tenemos dos opciones, una con el método `find` y la otra con `captures`.

Con `find`, la mejor opción en Rust de utilizar expresiones regulares, los resultados son:

Descripción                                            | Ejecución 1 | Ejecución 2 | Ejecución 3 | Ejecución 4 | Media
-------------------------------------------------------|-------------|-------------|-------------|-------------|---------
Rust opción más rápida (búsqueda por índice, no regex) | 29.436s     | 30.227s     | 33.716s     | 30.339s     | 30.929s
Python opción más rápida (regex match, una sola regex) | 271.780s    | 275.314s    | 274.713s    | 277.136s    | 274.736s
Rust regex más rápida (regex find e índices)           | 43.857s     | 44.913s     | 43.606s     | 49.675s     | 45.513s

Obteniendo un tiempo medio de 45.513s.

De utilizar el método `captures`, el cual era la opción con resultados más lentos en Rust, pero aun así mejores que en Python cuando comparamos expresiones regulares al inicio de este apartado, los resultados han sido:

Descripción                                            | Ejecución 1 | Ejecución 2 | Ejecución 3 | Ejecución 4 | Media
-------------------------------------------------------|-------------|-------------|-------------|-------------|---------
Rust opción más rápida (búsqueda por índice, no regex) | 29.436s     | 30.227s     | 33.716s     | 30.339s     | 30.929s
Python opción más rápida (regex match, una sola regex) | 271.780s    | 275.314s    | 274.713s    | 277.136s    | 274.736s
Rust regex más rápida (regex find e índices)           | 43.857s     | 44.913s     | 43.606s     | 49.675s     | 45.513s
Rust regex más lenta (regex captures, una sola regex)  | 348.511s    | 337.282s    | 340.437s    | 346.087s    | 343.079s

Es decir, una media de 343.079s (5min y 43.079s).

Puede leerse más sobre esta pérdida de velocidad en Rust respecto a Python en este hilo de [Reddit](https://www.reddit.com/r/rust/comments/5zit0e/regex_captures_slow_compared_to_python/).

Como conclusión, anteriormente vimos que la opción mas rápida de Rust fue 30.930s y en Python 4min y 36.736s. Con expresiones regulares, Rust puede hacer el análisis en 45.513s, el cual es mejor que Python, pero de utilizar el método de la expresión regular que da los resultados más lentos, se tiene un programa de menor velocidad que en Python, requiriendo 5min y 43.079s.

Terminar indicando que, los archivos obtenidos con Rust utilizando expresiones regulares y sin ellas, tienen el mismo `hash`, por lo que son iguales.

## Links de este tutorial

- [Siguiente apartado. Comparar memoria](09-compare-memory.html)
- [Página principal](introduction.html)

