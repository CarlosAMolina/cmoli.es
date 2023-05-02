# Comparar CPU

## Introducción

Otro aspecto a analizar de nuestro programa es el porcentaje de uso que realiza de CPU.

He buscado un programa que pudiera darme esta información, pero finalmente he utilizado el comando `ps` de Linux, aunque no parece que de unos resultados correctos, como veremos en este apartado.

## Herramienta elegida

Para obtener el uso de CPU creé un [script en bash](https://github.com/CarlosAMolina/nginx-logs/blob/main/measure/measure/measure-cpu) que guarda el resultado del comando `ps` en un archivo, muestro una parte:

```bash
ps_columns=cpuid,%cpu,%mem
echo CPU_ID CPU% MEM% TIME > $results_pathname
while :
do
  result=$(ps --no-headers -p $(pgrep $process_name) -o $ps_columns 2> /dev/null)
  if [ -n "$result" ]; then
    result="$result $(date +"%T.%N")"
    echo $result >> $results_pathname
    #echo $result
  fi
done
```

Este script analiza el proceso que se le indique. Al lanzar el archivo ejecutable de Rust, se crea solo un proceso que puede filtrarse por el nombre `nginx_logs`, y al lanzar el programa con Python, también se crea un solo proceso que, en este caso puede filtrarse por nombre `python`

El uso del comando `ps` no parece que de unos resultados muy fiables porque, en el caso de Rust, hay ocasiones en que solamente se mide un uso del 0% de CPU y hubo que realizar varias ejecuciones hasta obtener datos que poder representar. También, se ha intentado medir el uso de la CPU por núcleo, añadiendo para ello al comando `ps` la opción `cpuid` que muestra el ID del núcleo utilizado; pero, como veremos al comentar los resultados, no da unas mediciones correctas porque, cuando se tiene más de 100% de uso de CPU, no se muestra que se comience a utilizar un ID de CPU distinto.

Al igual que al estudiar la memoria, el script desarrollado ejecuta tres veces el programa, eliminando los archivos de resultados al final de cada proceso para que no afecte a los siguientes.

## Ejecutar medición

Los pasos son los mismos que al analizar la memoria, primero copiamos los archivos de logs en `/tmp/logs`, que es la ruta que el script estudiará:

```bash
cp -r ~/Software/poc-rust/logs /tmp/
```

Iniciamos las medidas, he cerrado los otros programas que pudieran estar funcionando para evitar que alteren las mediciones:

```bash
cd ~/Software/nginx-logs/measure/measure
./run-and-measure-cpu
```

Una vez las medidas han terminado, hay que modificar los archivos.

Para las mediciones de Python, cambiamos el nombre de los archivos resultado al formato `metrics-cpu-python-measure-1.txt`, cambiando el número final por el número de la medida, del 1 al 3.

Respecto a Rust, debido a que con el comando `ps` no siempre se tienen resultados porque el uso de CPU aparece en muchas ocasiones como 0%, el script que ejecutamos ha generado un total de 30 archivos de mediciones para que elijamos los que pueden aportar valor para una representación gráfica. Una vez elegimos tres archivos de medida, eliminamos las filas iniciales con medición 0% y cambiamos el nombre de los archivos, estos siguen la forma `metrics-cpu-nginx_logs-20230502-112147.txt`, los modificamos a `metrics-cpu-rust-measure-1.txt`, de nuevo, siendo el número del final el identificador de cada medición.

## Representación gráfica de las mediciones

Al igual que en el caso de la memoria, para representar los archivos de mediciones disponemos de unos scripts propios.

En la ruta `~/Software/nginx-logs/measure/measure/results` está el archivo `cpu-measure.tar.gz` con las medidas que he seleccionado del anterior apartado, podemos trabajar con ellas:

```bash
cd ~/Software/nginx-logs/measure/measure/results
tar xf cpu-measure.tar.gz
mv cpu-measure/* .
```

Recordemos que, utilizamos librerías externas de Python como `matplotlib`, por lo que activamos el entorno virtual con las librerías instaladas que creamos al representar los resultados de medir la memoria:

```bash
source ~/Software/nginx-logs/env/bin/activate
```

Cambiamos el directorio de trabajo y ejecutamos el script:

```bash
cd ~/Software/nginx-logs/measure/plot/
python src/plot_results.py cpu
```

Las gráficas se guardarán en la ruta ` ~/Software/nginx-logs/measure/plot/src/results/` como archivos `.png`.

## Resultados

Pueden verse los resultados en estas gráficas:

![](metrics-cpu-rust.png)

> CPU Rust

![](metrics-cpu-python.png)

> CPU Python

Rust utiliza como máximo cerca del 55% de CPU mientras que Python sigue necesitando más del 100% en algunos momentos.

Sobre el eje temporal, en el caso de Rust no corresponde con lo obtenido al analizar el tiempo de ejecución del programa ya que, como `ps` medía muchas veces la CPU como 0%, se eliminaron estos datos para tener una mejor gráfica a representar. Respecto a Python, hay una pequeña diferencia, vimos que el programa se ejecutaba en 9.7s, aquí la gráfica tiene datos hasta el segundo 10 porque habría un pequeño tiempo entre el inicio de medida de CPU y el inicio del programa.

Se ha investigado si Rust limita el uso de la CPU y creo que no existe esta limitación. He lanzado el programa con Rust con unos archivos de 1GB de tamaño y la CPU aumenta incluso más del 100%. Tampoco he encontrado en Internet que se indique esta limitación.

Sobre el intento de medir el uso de la CPU por núcleo, para los casos de Python donde se tienen valores mayores de 100%, vemos que el ID de la CPU sigue asignándose al mismo núcleo en lugar de a varios, por lo que creo que el comando `ps` no es fiable para mostrar el reparto entre núcleos:

```bash
CPU_ID CPU% TIME
...
3 99.7 11:35:56.632372690
3 99.8 11:35:56.645719645
3 100 11:35:56.659003978
3 100 11:35:56.672298553
3 100 11:35:56.685555299
3 100 11:35:56.698863741
3 100 11:35:56.712176948
3 100 11:35:56.725495465
3 100 11:35:56.738691330
3 101 11:35:56.751891343
3 101 11:35:56.765054441
3 101 11:35:56.778388529
...
3 105 11:35:57.165466589
3 105 11:35:57.178779176
3 106 11:35:57.192159432
3 106 11:35:57.205506248
3 106 11:35:57.218989264
3 106 11:35:57.232534075
3 106 11:35:57.245962912
3 106 11:35:57.259299157
3 106 11:35:57.272682696
3 96.3 11:35:57.286123093
...
```

## Links de este tutorial

- [Siguiente apartado. Compilación multiplataforma](11-cross-compilation.html)
- [Página principal](introduction.html)

