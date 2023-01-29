# Nginx configuración

## Contenidos


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

