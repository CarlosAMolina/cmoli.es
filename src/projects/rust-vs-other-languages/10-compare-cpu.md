# Comparar uso de CPU

Para analizar el uso de la CPU, he lanzado 3 veces consecutivas cada programa y medido la CPU utilizada al analizar unos ficheros de log, algunos comprimidos como `.gz`, son los mimso que los utilizados para medir el uso de memoria.

Rust utiliza el 55% de CPU mientras que Python sigue necesitando más del 100% en algunos momentos; es decir, Python utiliza 1 CPU totalmente y parte de otra. Rust,  en algunas ejecuciones se mantiene cerca de 0% durante más tiempo y en otras el incremento en el consumo de la CPU empieza antes

Se ha investigado si Rust limita el uso de la CPU y creo que no existe esta limitación. He lanzado el programa con Rust con unos archivos de 1GB de tamaño y la CPU aumenta incluso más del 100%. Tampoco he encontrado en Internet que se indique esta limitación.

Puede verse los resultados en estas gráficas:

![](metrics-cpu-rust.png)

> CPU Rust

![](metrics-cpu-python.png)

> CPU Python

Para obtener estos resultados, creé un [script en bash](https://github.com/CarlosAMolina/nginx-logs/blob/develop/measure/measure/measure-cpu) que guarda el resultado del comando `top` en un archivo, muestro una parte:

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

Este script analiza el proceso que le indique, he visto que al lanzar el programa con Python, se crea un solo proceso que se puede filtrar con `process_name` igual a `python` y al lanzar el binario de Rust, también se crea solo un proceso que filtro por el nombre `nginx_logs`. Lanzo el script que guarda esta información y ejecuto los programas por separado, no los dos a la vez, luego leo el archivo resultado y lo represento gráficamente gracias a otro [script](https://github.com/CarlosAMolina/nginx-logs/blob/develop/measure/plot/src/plot_results.py).


Se ha intentado medir el uso de la CPU por núcleo. Para medirlo se añade al comando `ps` la opción `cpuid` que muestra el id del núcleo utilizado, veo que al haber valores mayores de 100%, sigue asignándolo a un núcleo en lugar de a varios, por lo que creo que este comando no es fiable para mostrar el reparto entre núcleos:

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
