# Instalación Rust y Python

## Contenidos

## Introducción

Como el programa desarrollado está escrito en Rust y Python, lo primero que necesitamos es instalar estos lenguajes de programación en nuestro equipo.

Otro aspecto también a cubrir es disponer de un editor de código donde poder abrir los archivos del programa.

¡Vamos a ello!

## Instalación

En lugar de hacer un tutorial que explique paso a paso la instalación, muestro unos enlaces donde tenemos esta información para todos los sistemas operativos.

### Instalación Rust

Para la instalación de Rust, seguiremos lo indicado en este [enlace](https://www.rust-lang.org/tools/install) de su página oficial, de este modo instalaremos:

- Rustup: sirve para instalar el lenguaje Rust.
- Cargo: crea proyectos en lenguaje Rust y hace las funciones de package manager.

#### Instalación Rust por primera vez en el equipo

Accediendo al [enlace](https://www.rust-lang.org/tools/install), abriremos una página web que detecta nuestro sistema operativo y explica el proceso de instalación utilizando Rustup.

#### Actualizar la versión de Rust

En caso de tener ya instalado Rust, podemos actualizarlo a la última versión con este comando:

```bash
rustup update
```

### Instalación Python

Es el turno de instalar Python.

La versión escogida es Python 3.11.3 ya que, en la versión 3.11 se introdujeron [mejoras en su velocidad](https://docs.python.org/3.11/whatsnew/3.11.html#faster-cpython).

#### Instalación Python por primera vez en el equipo

Si bien desde [la web oficial de Python](https://www.python.org/downloads/) podemos instalar las distintas versiones de Python para diferentes sistemas operativos, recomiendo seguir [este enlace de Real Python](https://realpython.com/installing-python/) con los puntos necesarios en cada sistema operativo.

#### Instalar una versión diferente de Python

También, es posible tener diferentes versiones de Python en nuestro equipo, para ello puede seguirse los pasos de [este enlace](https://cmoli.es/wiki/python/python.html#de-manera-manual).

### Comprobar la instalación

En los enlaces anteriores tenemos que, para verificar la correcta instalación, podemos ejecutar estos comandos en la terminal:

- Rust

Mostrar versión de Rust instalada:

```bash
$ rustc --version
rustc 1.69.0 (84c898d65 2023-04-16)
```

Versión de Cargo:

```bash
# https://www.rust-lang.org/learn/get-started
$ cargo --version
cargo 1.69.0 (6e9a83356 2023-04-12)
```

- Python

Para mostrar la versión de Python instalada:

```bash
$ python --version
Python 3.11.3
```

## Editor de Código

Al igual que con la instalación, en este apartado comparto algunos enlaces que pueden ayudar a elegir el editor de texto que mejor se ajuste a nuestras necesidades y conocimientos.

### Editor de código para Rust

Unas de las opciones más cómodas pueden ser los [productos de JetBrains](https://www.jetbrains.com/rust/), y en la [web oficial de Rust](https://www.rust-lang.org/learn/get-started) en la sección `Other tools` tenemos más opciones disponibles para otros editores.

### Editor de código para Python

De nuevo, la opción más sencilla es quizá [PyCharm de JetBrains](https://www.jetbrains.com/pycharm/), aunque disponemos de muchas otras posibilidades, como puede verse en [el siguiente artículo de Real Python](https://realpython.com/python-ides-code-editors-guide/).

## Recursos

Editor de código Python:

- PyCharm de JetBrains:

  <https://www.jetbrains.com/pycharm/>

- Otros editores:

  <https://realpython.com/python-ides-code-editors-guide/>

Editor de código Rust:

- JetBrains:

  <https://www.jetbrains.com/rust/>

- Otros editores (sección `Other tools`):

  <https://www.rust-lang.org/learn/get-started>

Instalación Python:

<https://realpython.com/installing-python/>

Instalación Rust, web oficial:

<https://www.rust-lang.org/tools/install>

Verificar instalación Rust y crear proyecto de prueba:

<https://www.rust-lang.org/learn/get-started>

Versiones Python, web oficial:

<https://www.python.org/downloads/>

## Links de este tutorial

- [Página principal](introduction.html)
- [Siguiente apartado. Comparar código Rust y Python](05-compare-code.html)
