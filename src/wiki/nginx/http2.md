# Nginx HTTP2

## Introducción

Diferencias con HTTP1:

- HTTP1 es un protocolo que envía la información como texto mientras que HTTP2 lo hace en formato binario, lo que reduce los errores.
- HTTP2 comprime las cabeceras de respuesta, lo que reduce los tiempos de transferencia.
- HTTP2 utiliza conexiones persistentes y multiplex streaming. Con HTTP1 cada recurso (archivo html y las imágenes, estilos css, código js que utiliza, etc.) solicitado necesita una petición distinta (simple streaming), lo que implica tiempo para iniciarla y terminarla. Por el contrario, HTTP2 crea una conexión y en ella se envían varios recursos, ya que en un string de datos binario puede comprimirse; por ejemplo, la conexión pide el html y luego en la misma conexión se piden los recursos css, js, etc. que necesita y estos se envían juntos.
- HTTP2 puede utilizar server push, es decir, que en la respuesta en que se envía el archivo html, también se envíen los archivos css, js, etc. asociados.

## Configuración

### Instalación y activación

HTTP2 necesita:

- Instalar el módulo `http_v2_module` de Nginx.
- SSL.

Ejemplo de configuración:

```bash
http {
    server {
        listen 443 ssl http2;
        ....
    }
}
```

Con esto, al ver las peticiones en nuestro navegador web, podemos ver la versión HTTP/2.

La mayoría de navegadores soporta HTTP2; en caso contrario, la página se devolverá como HTTP1.

Ejemplo:

```bash
$ curl -Ik https://localhost:8080/
HTTP/2 200
...
```

### Evitar escuchar HTTP

Aunque tengamos HTTP2 funcionando, si al acceder a la URL con HTTP en lugar de HTTP2 esta devuelve respuesta, podemos evitarlo redirigiendo todas las peticiones HTTP a HTTP2, una manera de conseguirlo es añadir un nuevo server context:

```bash
# Redirect all trafic to HTTPS.
server {
    listen 80;
    server_name localhost;
    return 301 https://$server_name$request_uri;
}
```

De la anterior configuración:

- `server_name`: posee el mismo valor que el que tengamos para el context server con puerto 443.
- En lugar de `host` podemos utilizar `$server_name` o el mismo valor que en `server_name` (IP o dominio).
