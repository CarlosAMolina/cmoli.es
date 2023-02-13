# SSL

## Self certificate

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

## Configurar SSL en Nginx

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

