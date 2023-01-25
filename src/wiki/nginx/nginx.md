# Nginx

## Instalación

### Debian

```bash
sudo apt install nginx
```

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

## Iniciar servidor

```bash
sudo systemctl start nginx.service
```

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

## Cambiar ruta de los contenidos a mostrar

Si queremos mostrar los archivos que tengamos en la ruta `/home/foo/bar/public_html/`, modificaremos el siguiente archivo:

```bash
sudo vi /etc/nginx/sites-available/default
```

En la sección `server`, para root indicaremos el path deseado:

```bash
server {
    root /home/foo/bar/public_html;
}
```

Reiniciamos el servicio Nginx:

```bash
sudo nginx -s reload
```

Desde el navegador web, para visualizar por ejemplo al archivo que tengamos en `/home/foo/bar/public_html/index.html`, accedemos a `http://1.2.3.4./index.html`. 

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

