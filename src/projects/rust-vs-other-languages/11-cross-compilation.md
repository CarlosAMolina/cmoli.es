# Compilación multi plataforma

Al crear el archivo binario Rust con el comando `cargo build --target` hay que especificarle la arquitectura destino, al analizar el espacio en disco necesario, utilicé como `target` a `x86_64-unknown-linux-musl`, pero de generar el binario para otra arquitectura, ay que especificarla o no funcionará.

Por ejemplo, para ARM y x86 pueden listarse las posibilidades existentes con el siguiente comando:

```bash
$rustc --print target-list | grep -E 'arm-|x86_'
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

