# Compilación multiplataforma

## Introducción

Rust permite generar el programa ejecutable para distintas plataformas; pero, como indica su [documentación](https://rust-lang.github.io/rustup/cross-compilation.html#cross-compilation), es necesario instalar software adicional.

Al crear el archivo ejecutable para una plataforma específica, debe indicase el objetivo con el comando `cargo build --target`. Por ejemplo, para ARM y x86 pueden listarse las posibilidades existentes con el siguiente [comando](https://doc.rust-lang.org/rustc/targets/built-in.html):

```bash
$ rustc --print target-list | grep -E 'arm-|x86_'
arm-linux-androideabi
arm-unknown-linux-gnueabi
arm-unknown-linux-gnueabihf
arm-unknown-linux-musleabi
arm-unknown-linux-musleabihf
x86_64-apple-darwin
x86_64-apple-ios
x86_64-apple-ios-macabi
...
x86_64-unknown-l4re-uclibc
x86_64-unknown-linux-gnu
x86_64-unknown-linux-gnux32
x86_64-unknown-linux-musl
...
```

En este apartado, comentaré cómo generé un archivo ejecutable desde unas plataformas a otras.

## Proceso

En [este repositorio de GitHub](https://github.com/CarlosAMolina/rust/tree/master/cross-compilation) se creó un pequeño programa para compilarlo a distintas plataformas, en su archivo README pueden verse más detalles.

Comento dos maneras distintas en que se abordó este proceso.

### De Arch Linux a Debian

Desde un sistema Arch Linux se compiló el programa para ser utilizado en Debian, el proceso consistió en utilizar una imagen Docker que compilara el archivo ejecutable para la plataforma destino.

### De Ubuntu a MacOS

En el caso de compilar el ejecutable para MacOs desde Ubuntu, hubo que instalar un proyecto de GitHub adicional, los pasos se describen en [este artículo](https://wapl.es/rust/2019/02/17/rust-cross-compile-linux-to-macos.html).

## Conclusiones

En esta sección se ha comentado de manera breve diferentes modos de compilar el programa para una plataforma distinta a la del host anfitrión. Lo que ha querido resaltarse es que, crear un archivo ejecutable con Rust de una arquitectura a otra, no es un proceso inmediato, sino que hay que realizar unos pasos previos como instalar software adicional.

## Links de este tutorial

- [Siguiente apartado. Otros aspectos](12-other-aspects.html)
- [Página principal](introduction.html)

