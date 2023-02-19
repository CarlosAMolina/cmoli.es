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

### Certificado SSL autoformidado

Es un certificado creado y firmado por nosotros.

Podemos generarlo con el siguiente comando; cuando lo ejecutemos, deberemos responder unas preguntas, podemos dejar las opciones por defecto.

```bash
mkdir /tmp/ssl
openssl req -x509 -nodes -days 1 -newkey rsa:2048 -keyout /tmp/ssl/nginx-selfsigned.key -out /tmp/ssl/nginx-selfsigned.crt
```

Del comando anterior:

- req: pedir un certificado.
- x509: el estándar solicitado.
- days: número de días para los que el certificado será válido.
- nodes: evitar passphrase o password para el key file.
- newkey rsa:2048: generar una nueva private key, de tipo rsa de 2048 bytes.
- keyout: dónde guardar la clave privada.
- out: dónde guardar el certificado.

Documentación del comando en este [link](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04).

#### Configurar SSL en Nginx

Indicamos el puerto y el módulo a utilizar por la directiva listen:

```bash
...
http {
    ...
    server {
        listen 443 ssl;
        ...
        ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;
    }

}
...
```

Para hacer petición con curl, es necesario permitir el certificado autofirmado mediando la opción `k`:

```bash
curl -Ik https://localhost:8080/
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

### Mejorar la seguridad

#### Deshabilitar SSL

En este apartado cómo mejorar el cifrado de las conexiones.

Respecto el protocolo que cifra las conexiones, el protocolo SSL (Secure Sockets Layer) ha sido reemplazado por TLS (Transport Layer Security).

Configuración:

```bash
server {
    ...
    # Disable SSL.
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    # Optimise cipher suits.
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

    # Enable DH Params.
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    # Enable HSTS.
    add_header Strict-Transport-Security "max-age=31536000" always;

    # SSL sessions.
    ssl_session_cache shared:SSL:40m;
    ssl_session_timeout 4h;
    ssl_session_tickets on;
    ...
}
```

De la anterior configuración:

- `ssl_protocols`: de no especificarlos, Nginx tiene configurados valores por defecto ([link](https://nginx.org/en/docs/http/configuring_https_servers.html#compatibility)).
- `ssl_ciphers`: cada uno es separado con `:`, para no usar un cipher, utilizamos `:!`. Esta configuración va cambiando por el tiempo (pueden encontrarse bugs, etc) por lo que hay que buscar una fuente fiable y utilizar los valores que mejor resultados den en la actualidad. De no especificarlos, Nginx tiene configurados valores por defecto ([link](https://nginx.org/en/docs/http/configuring_https_servers.html#compatibility)).
- `ssl_dhparam`: mejora la seguridad en el intercambio de keys entre el cliente y el servidor. Artículos sobre esto en [link](https://hackernoon.com/algorithms-explained-diffie-hellman-1034210d5100) y [link](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange). Para generar el archivo necesario, utilizamos `openssl` (documentación en este [link](https://wiki.archlinux.org/title/OpenSSL)).

    ```bash
    openssl dhparam -out /tmp/dhparam.pem 2048
    ```

    Del anterior comando:
    - Tamaño 2048: debe coincidir con el valor que utilizamos para crear la clave privada en el certificado SSL autofirmado.

- `add_header Strict-Transport-Security`: cabecera que indica al navegador no cargar nada por HTTP. Esto minimiza las redirecciones del puerto 80 al 443. El valor de `max-age` son segundos. Documentación en el [link](https://developer.mozilla.org/es/docs/Web/HTTP/Headers/Strict-Transport-Security).
- `ssl_session_cache`. Documentación en este [link](https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_session_cache). Guarda en caché los handshakes SSL durante el tiempo especificado, lo que hace las conexiones más rápidas. Sus opciones son:
  - Cómo realizar el caché:
      - `builtin`: específico para un worker process, no muy útil
      - `shared`: la sesión cacheada puede ser utilizada por cualquier worker process.
  - `SSL`: nombre dado al caché (para tipo `shared`).
  - 40m: tamaño del caché de tipo `shared` en bytes (la configuración de la caché `builtin` cambia un poco).
- `ssl_session_timeout`: tiempo que mantener una sesión cacheada.
- `ssl_session_tickets`: ofrece mejor rendimiento ya que es un modo de identificar la sesión SSL del navegador web y evitar leer las sesiones cacheadas del servidor para identificarla.
