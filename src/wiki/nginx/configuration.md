# Nginx configuración

## Contenidos

## Términos utilizados en archivos de configuración

Estos términos se utilizan en archivos como por ejemplo, en el `nginx.conf`.

Hay dos términos a diferenciar en la configuración de Nginx: context y `directive`.

[Recursos](https://bbvanext.udemy.com/course/nginx-fundamentals).

### Context

Son secciones en la configuración. Ejemplo:

```bash
http {
   ...
}
```

En estas secciones se indican los `directive`.

Cada context puede contener otros context que heredan del context padre.

El context superior es el propio archivo de configuración, llamado `main context`.

#### Context más importantes

- http: configura lo relacionado con HTTP.
- server: donde definimos un host virtual.
- location: para gestionar/buscar términos en las peticiones que recibe el servidor.

### Directive

Son opciones de configuración específicas utilizadas en los archivos, formados por un nombre y un valor. Por ejemplo:

```bash
server_name foo.com;
```

En el `main context` configuramos `directives` globales que aplican a todos los procesos.

## Editar archivo `nginx.conf`

En esta sección veremos cómo editar el archivo `nginx.conf`, podemos borrar todo su contenido e ir añadiendo lo que veremos a continuación, donde se describe cómo configurar cada context.

### events

Aunque esté vacío, es necesario dejarlo en el archivo para tener una configuración válida:

```bash
event {}
```

### http

#### server

En los archivos de configuración, los context `server` dentro del context `http` se conocen como `virtual host`.

Los `virtual host` se utilizan para ofrecer contenido que se encuentra en una ruta de nuestro servidor.

Se encargan de escuchar en un puerto.

Estudiaremos el siguiente ejemplo:

```bash
server {
    listen 80;
    server_name 1.2.3.4;

    root /home/foo/bar/public_html;
}
```

##### Directive `listen`

Especifica el puerto que escucha.

##### Directive `server_name`

Configura el dominio, sudominio o ip para el que aplica el context `server`.

Puede aceptar wildcards como el asterisco, por ejemplo `*.foo.com` aceptará conexiones de cualquier subdominio, como `www.foo.com`, `images.foo.com`, etc.

##### Directive `root`

Es el `path` principal desde el que Nginx gestionará las peticiones.

Por ejemplo, de recibir la petición `/images/dog.png`, Nginx buscará en `/home/foo/bar/public_html/images/dog.png`.


Verificamos que la configuración es correcta (ver apartado con los comandos) y reiniciamos el servicio `nginx`

```bash
sudo nginx -t
```

Desde el navegador web, visualizamos por ejemplo al archivo que tengamos en `/home/foo/bar/public_html/index.html` accediendo a `http://1.2.3.4./index.html`.

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

