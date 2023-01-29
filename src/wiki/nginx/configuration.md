# Nginx configuración

## Contenidos

## Términos utilizados en archivos de configuración

Estos términos se utilizan en archivos como por ejemplo, en el `nginx.conf`.

Deben diferenciarse dos términos en la configuración de Nginx: `context` y `directive`.

[Recursos](https://bbvanext.udemy.com/course/nginx-fundamentals).

### Context

Son secciones en la configuración. Ejemplo:

```bash
http {
   ...
}
```

En estas secciones se indican los `directive`.

Cada `context` puede contener otros `context` que heredan del `context` padre.

El `context` superior es el propio archivo de configuración, llamado `main context`.

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

## Cambiar ruta del contenido a mostrar

Si queremos mostrar los archivos que tengamos en la ruta `/home/foo/bar/public_html/`, modificaremos el siguiente archivo:

```bash
sudo vi /etc/nginx/sites-available/default
```

En la sección `server`, para `root` indicaremos el path deseado:

```bash
server {
    root /home/foo/bar/public_html;
}
```

Verificamos que la configuración es correcta (ver apartado con los comandos) y reiniciamos el servicio `nginx`

```bash
sudo nginx -t
```

Desde el navegador web, visualizamos por ejemplo al archivo que tengamos en `/home/foo/bar/public_html/index.html` accediendo a `http://1.2.3.4./index.html`.

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

