# Especificaciones del equipo

## Contenidos

- [Introducción](#introducción)
- [Características](#características)
- [Versiones de Software](#versiones-de-software)
- [Comandos utilizados](#comandos-utilizados)
- [Recursos](#recursos)
- [Links de este tutorial](#links-de-este-tutorial)

## Introducción

Para tener una idea de los resultados que se conseguirían dependiendo del equipo utilizado, a continuación muestro las características del ordenador con el que he trabajado. Así podéis saber si en vuestro equipo de mejores especificaciones obtendríais unos resultados más eficientes que los dados en los apartados de este proyecto.

## Características

- CPU:
  - Modelo: Intel(R) Core(TM) i5-4440 CPU @ 3.10GHz
  - Arquitectura: x86_64
  - CPU(s): 4. Detalles:
    - Socket(s): 1
    - Núcleo(s) por socket: 4
    - Hilo(s) de procesamiento por núcleo: 1
  - Velocidad del reloj:
    - Máxima: 3.300,0000 MHz
    - Mínima: 800,0000 MHz
  - Caché:
    - L1d: 128 KiB
    - L1i: 128 KiB
    - L2: 1 MiB
    - L3: 6 MiB
- Memoria:
  - RAM: 7.887,4 MiB
  - Swap: 12.288,0 MiB
- Sistema operativo: Arch Linux
- Kernel:
  - Nombre: Linux
  - Release: 6.2.13-arch1-1
  - Versión: #1 SMP PREEMPT_DYNAMIC Wed, 26 Apr 2023 20:50:14 +0000

## Versiones de Software

Las versiones analizadas de Rust y Python han sido:

- Rust: rustc 1.69.0 (84c898d65 2023-04-16)
- Python: 3.11.3

También, se ha utilizado Docker:

- Docker: 23.0.4, build f480fb1e37

## Comandos utilizados

Para obtener algunas de las anteriores características, los comandos utilizados han sido los siguientes:

- CPU: `lscpu`.
- Memoria: `top`.
- Sistema operativo: `cat /etc/os-release`.
- Kernel:
  - Nombre: `uname`.
  - Release: `uname -r`.
  - Versión: `uname -v`.

## Recursos

Obtener características CPU:

<https://linuxhandbook.com/check-cpu-info-linux/>

Mostrar memoria:

<https://www.cyberciti.biz/faq/how-to-check-memory-debian-linux/>

Ver información del sistema operativo:

<https://linuxize.com/post/how-to-check-your-debian-version/>

Mostrar datos del Kernel:

<https://vitux.com/get-debian-system-and-hardware-details-through-the-command-line/>

  - Kernel release vs kernel version:

    <https://unix.stackexchange.com/questions/124466/what-is-the-difference-of-kernel-distributions-release-and-version>

## Links de este tutorial

- [Siguiente apartado. Instalación Rust y Python](04-install-rust-and-python.html)
- [Página principal](introduction.html)

