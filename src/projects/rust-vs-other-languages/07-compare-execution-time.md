# Comparar tiempo de ejecución

## Introducción

En este apartado veremos el tiempo que requiere cada programa para procesar los logs creados en el apartado anterior.

## Consideraciones iniciales

Empezamos comentando algunos puntos a tener en cuenta a la hora de escribir el programa.

### Opciones más eficientes en Rust

Para realizar las operaciones en Rust, es necesario investigar qué método da resultados más eficientes. Por ejemplo:

- Al escribir los resultados en un archivo, para nuestro caso ayuda utilizar BufWriter ya que, como indica [la documentación](https://doc.rust-lang.org/std/io/struct.BufWriter.html), puede mejorar la velocidad en programas que realizan pequeñas y repetidas llamadas de escritura al mismo archivo.
- Si utilizamos expresiones regulares, hay que evitar perder tiempo por compilar varias veces la misma expresión regular, para ello [la documentación](https://docs.rs/regex/1.5.4/regex/index.html#example-avoid-compiling-the-same-regex-in-a-loop) recomienda utilizar el crate `lazy_loading`.

En el caso de Python, para evitar la pérdida de tiempo por repetir la compilación de la expresión regular, se utiliza [re.compile](https://docs.python.org/3/library/re.html#re.compile).

Tanto en Rust como Python, el obtener las partes que componen un log cuenta con diversas opciones y algunas son más óptimas que otras, las analizamos en la siguiente sección.

### Obtener partes del log

Al haber diferentes modos de parsear logs, es necesario buscar la opción más óptima. Para ello, en mi cuenta de GitHub he creado unas pruebas en las que obtengo los valores de parser un log 5.000 veces utilizando:

- Expresiones regulares: comparando diferentes opciones que proporcionan para encontrar los resultados.
- Sin utilizar expresiones regulares, se buscan los caracteres que indican el fin de cada componente del log (ip remota, usuario remoto, hora, etc...) y se tiene en cuenta el número de caracteres hasta el siguiente elemento.

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

Para estos resultados se ha utilizado:

- Resultado `match`, la función empleada es [is_match](https://docs.rs/regex/latest/regex/struct.Regex.html#method.is_match), no sirve para obtener los valores que cumplen la expresión regular, pero si para saber si la expresión regular tiene resultados o no.
- Resultado `find`, la función utilizada es [find](https://docs.rs/regex/latest/regex/struct.Regex.html#method.find), devuelve la posición de inicio y fin del primer resultado (el de más a la izquierda) en el string. Es el equivalente a la función `search` de Python. Por lo que se van buscando los elementos del log teniendo en cuenta la posición del anterior encontrado.
- Resultado `captures`, en este caso empleamos la función [captures](https://docs.rs/regex/latest/regex/struct.Regex.html#method.captures), con la que obtenemos todos los elementos con una sola expresión regular, guardados en grupos.
- Resultado `with no regex`, no hace uso de expresiones regulares, recorre el string en busca de la posición de los caracteres que indican el fin de cada elemento del log y suma el número de posiciones hasta el siguiente.
- Resultado `with no regex one loop`, igual que `with no regex` pero guarda los caracteres a buscar en un array que recorre con un loop.

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

- Resultado `match`, utiliza la función [re.match](https://docs.python.org/3/library/re.html#re.match) que solo busca si la expresión regular se cumple al inicio del string analizado, por lo que cada vez que se detecta un elemento del log, para buscar el siguiente se analiza el string desde la última posición del elemento encontrado.
- Resultado `search`, emplea la función [re.search](https://docs.python.org/3/library/re.html#re.search) que busca la primera coincidencia (la que hay más a la izquierda del string) de la expresión regular en cualquier posición del string; el modo de encontrar cada elemento es igual que para `match`.
- Resultado `match groups`, la función utilizada es [re.match](https://docs.python.org/3/library/re.html#re.match) pero se le pasa una expresión regular que busca todos los elementos a la vez, cada uno guardado en un grupo.
- Resultado `search groups`, igual que para `match groups` pero la función empleada es [re.search](https://docs.python.org/3/library/re.html#re.search).
- Resultado `without regex`: se buscan elementos que determinan el fin de cada parte del log y se tiene en cuenta el número de caracteres hasta el siguiente.

En el caso de Python, los mejores resultados se tienen con la opción `match` de las expresiones regulares utilizando una expresión regular que capture todos los elementos de una vez, mientras que en Rust es mejor no utilizar expresiones regulares. Estas serán las maneras en que parsearemos los logs.

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

Es verdad que, al analizar la manera más rápida de parsear logs, Rust era más rápido que Python con expresiones regulares, pero porque solo analizamos un log, de trabajar con los archivos anteriores, daría como resultado un peor programa que su versión en Python.

Para ver esto, debemos cambiar los siguientes archivos del programa en Rust:

- Archivo `Cargo.toml`. Añadir en `[dependencies]`:

```bash
lazy_static = "1.4.0"
regex = "1.5.6"
```

- Archivo `src/m_log.rs`:

Descomentar:

```bash
use lazy_static::lazy_static;
use regex::Regex;
```

Comentar la función `get_log` utilizada actualmente y descomentar la función `get_log` que utiliza expresiones regulares, tenemos dos opciones, una con la función `find` y la otra con `captures`.

Con `find`, la mejor opción en Rust de utilizar expresiones regulares, los resultados son:

- Ejecución 1: 43.856874086s
- Ejecución 2: 44.913219761s
- Ejecución 3: 43.605705085s
- Ejecución 4: 49.675238313s

La media es de 45.51275931125s

El método utilizado ha sido `captures`, la cual era la opción con resultados más lentos en Rust, pero aun así mejores que en Python cuando comparamos expresiones regulares al inicio de este apartado.

Los resultados han sido:

- Ejecución 1: 348.511046044s
- Ejecución 2: 337.281804016s
- Ejecución 3: 340.43731135s
- Ejecución 4: 346.087355349s

Es decir, una media de 343.07937918975006s (5min y 43.079s).

Anteriormente, la opción mas rápidas de Rust fue 30.930s y en Python 4min y 36.736s. Con expresiones regulares Rust puede tener hacer el análisis en 45.513s, el cual es mejor que Python, pero de utilizar la función de la expresión regular que da los resultados más lentos, se tiene un programa de menor velocidad que en Python.

Los archivos obtenidos con Rust utilizando expresiones regulares y sin ellas, tienen el mismo `hash`, por lo que son iguales.
