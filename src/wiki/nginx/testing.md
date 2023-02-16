# Testing

## Apache Benchmark

Sirve para conocer el comportamiento del servidor al responder a las peticiones.

Documentación en el siguiente [link](https://httpd.apache.org/docs/2.4/programs/ab.html).

Ejemplo, para enviar 100 peticiones, 10 concurrentes:

```bash
ab -n 100 -c 10 http://localhost
```

De los resultados del anterior comando, destacar los `Request per second` y `Time per request`, este último es el tiempo medio en recibir respuesta para una petición.

## nghttp2

### ngttp2 introducción

Es una implementación del protocolo HTTP2, que ofrece entre otras opciones, un cliente.

### nghttp2 enlaces

Página oficial, [link](https://nghttp2.org/).
Código, [link](https://nghttp2.org/).

#### nghttp2 instalación

```bash
wget https://github.com/nghttp2/nghttp2/releases/download/v1.52.0/nghttp2-1.52.0.tar.bz2
tar xfv nghttp2-1.52.0.tar.bz2
cd nghttp2-1.52.0/
./configure
make
```

#### nghttp2 uso

```bash
./src/nghttp -nysa http://localhost/index.html
```

Opciones utilizadas:

- n: descartar las respuestas, ya que no queremos guardarlas.
- y: ignorar certificado autofirmado.
- s: mostrar las estadísticas de las respuestas.
- a: solicitar los archivos asociados al archivo html (css, imágenes, etc), de no utilizar esta opción, solo se descargaría el html.

### nghttp2 ejemplo

Puede verse un ejemplo de uso y sus resultados en la sección server push de Nginx.

