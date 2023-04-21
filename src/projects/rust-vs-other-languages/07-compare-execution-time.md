# Comparar tiempo de ejecución

## Introducción

En este apartado veremos el tiempo que requiere cada programa para procesar los logs creados en el apartado anterior.

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

## Python más rápido que Rust

Para hacer esta comparación, en cada lenguaje se ha utilizado la manera de parsear los logs mas rápida. En Python esto se consigue con expresiones regulares, mientras que en Rust es mejor ir buscando caracteres que identifiquen el final de cada campo.

TODO comprobar que el anterior párrafo es verdad, poner enlace al repo en GitHub donde comparo distintos métodos en los lenguajes.

En el caso de utilizar expresiones regulares, Rust tarda más que Python, para verlo, modificamos el código del siguiente modo:

TODO
