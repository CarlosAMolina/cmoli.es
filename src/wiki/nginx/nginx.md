# Nginx

## Contenidos


## Páginas web Nginx

- <https://nginx.org/>: contiene documentación, descargas, etc.
- <https://www.nginx.com/>: página principal, también incluye documentación

## Instalación

Ver [apartado instalación](installation.html).

## Módulos

Los módulos amplían las funcionalidades del servidor.

Solo pueden utilizarse de instalarse Nginx mediante `building from sources`.

Hay dos tipos:

- Módulos que vienen en el código de Nginx: ver sección `Modules reference` en [link]<https://nginx.org/en/docs/>.
- Módulos de terceras partes: <https://www.nginx.com/resources/wiki/modules/>

## Comandos del servidor

Los comandos sobre parar, iniciar, etc. el servidor también puede realizarse con `systemctl` (ver apartado instalación).

### Listar comandos disponibles

```bash
nginx -h
```

### Iniciar servidor

```bash
sudo nginx
```

Verificamos su funcionamiento:

```bash
ps aux | grep nignx
```

### Parar servidor

```bash
sudo nginx -s quit
# Option `stop` executes a fast shutdown and option `quit` a graceful one.
```

[Recursos](https://nginx.org/en/docs/beginners_guide.html)

### Verificar configuración es correcta

```bash
sudo nginx -t
```

### Reiniciamos el servicio `nginx`:

```bash
sudo nginx -s reload
```

## Configuración

Ver apartado [configuración](configuration.html).

