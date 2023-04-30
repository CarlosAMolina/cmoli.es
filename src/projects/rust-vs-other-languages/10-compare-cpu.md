# Comparar CPU

## Introducción

Otro aspecto a analizar de nuestro programa es el porcentaje de uso que realiza de CPU.

He buscado un programa que pudiera darme esta información pero finalmente he utilizado el comando `ps` de Linux, aunque, al ver el uso de CPU por núcleo, no parece que de unos resultados correctos, como veremos en este apartado.

## Herramienta elegida

Para obtener el uso de CPU creé un [script en bash](https://github.com/CarlosAMolina/nginx-logs/blob/develop/measure/measure/measure-cpu) que guarda el resultado del comando `ps` en un archivo, muestro una parte:

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

Se ha intentado medir el uso de la CPU por núcleo. Para medirlo se añade al comando `ps` la opción `cpuid` que muestra el ID del núcleo utilizado; pero, como veremos al comentar los resultados, no parece dar unas mediciones correctas.

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

## Representación gráfica de las mediciones

De nuevo, como en el caso de la memoria, para representar los archivos de mediciones disponemos de unos scripts propios:

```bash
cd ~/Software/nginx-logs/measure/plot/
```

Recordemos que utilizamos librerías externas de Python como `matplotlib`, por lo que activamos el entorno virtual con las librerías instaladas que creamos al representar los resultados de medir la memoria:

```bash
source ~/Software/nginx-logs/env/bin/activate
```

Ejecutamos el script:

```bash
python src/plot_results.py
```

Las gráficas se guardarán en la ruta ` ~/Software/nginx-logs/measure/plot/src/results/` como archivos `.png`.

## Resultados

Rust utiliza el 55% de CPU mientras que Python sigue necesitando más del 100% en algunos momentos; es decir, Python utiliza 1 CPU totalmente y parte de otra. Rust en algunas ejecuciones se mantiene cerca de 0% durante más tiempo y en otras el incremento en el consumo de la CPU empieza antes

Se ha investigado si Rust limita el uso de la CPU y creo que no existe esta limitación. He lanzado el programa con Rust con unos archivos de 1GB de tamaño y la CPU aumenta incluso más del 100%. Tampoco he encontrado en Internet que se indique esta limitación.

Puede verse los resultados en estas gráficas:

![](metrics-cpu-rust.png)

> CPU Rust

![](metrics-cpu-python.png)

> CPU Python

Sobre el intento de medir el uso de la CPU por núcleo, se tienen valores mayores de 100% para los que se asignan a un núcleo en lugar de a varios, por lo que creo que este comando no es fiable para mostrar el reparto entre núcleos:

```bash
CPU_ID CPU% TIME
...
3 95.0 18:23:28.290094341
3 97.0 18:23:28.300933372
3 98.0 18:23:28.311733453
3 99.0 18:23:28.322591223
3 100 18:23:28.333508142
3 101 18:23:28.344307124
3 102 18:23:28.355119871
3 103 18:23:28.365830772
3 104 18:23:28.376639765
3 105 18:23:28.387359956
3 106 18:23:28.398142936
3 107 18:23:28.408946173
3 109 18:23:28.420047112
...
```

## Links de este tutorial

- [Siguiente apartado. Compilación multiplataforma](11-cross-compilation.html)
- [Página principal](introduction.html)

