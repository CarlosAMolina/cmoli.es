# Nginx

## Contenidos


## Páginas web Nginx

- <https://nginx.org/>: contiene documentación, descargas, etc.
- <https://www.nginx.com/>: página principal, también incluye documentación

## Instalación

### Instalación en Debian

#### Instalación en Debian desde repositorios oficiales

Es recomendable realizar la instalación mediante `building from sources` para tener la última versión, más opciones de configuración y añadir módulos.

```bash
sudo apt install nginx
```

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

#### Instalación en Debian building from sources

Deben realizarse los siguientes apartados en orden.

[Recursos](https://bbvanext.udemy.com/course/nginx-fundamentals)

##### Descargar código

Desde este [link](https://nginx.org/en/download.html) descargamos la rama `mainline`, que es la [que recomiendan](https://www.nginx.com/blog/nginx-1-18-1-19-released/) ya que la rama `stable` se actualiza con menor regularidad:

```bash
wget https://nginx.org/download/nginx-1.23.3.tar.gz
tar -zxvf nginx-1.23.3.tar.gz
cd nginx-1.23.3
```

##### Instalar requisitos

Ejecutamos el comando.

```bash
./configure
```

Iremos obteniendo errores de librerías que necesitamos instalar:

```bash
# Error por no tener instalado compilador
sudo apt install build-essential
# Falta librería PCRE
sudo apt install libpcre3 libpcre3-dev
# Falta librería zlib
sudo apt install zlib1g zlib1g-dev
# Para dar soporte a https (esto no se mostrará como error de algo faltante)
sudo apt install libssl-dev
```

##### Configurar instalación

Las opciones de configuración disponibles se ven con:

```bash
./configure --help
```

La descripción de cada opción puede consultarse en este [link](https://nginx.org/en/docs/configure.html).

Realizamos la configuración:

```bash
./configure \
    --sbin-path=/usr/local/nginx \
    --conf-path=/usr/local/nginx/nginx.conf \
    --error-log-path=/usr/local/nginx/logs/error.log \
    --http-log-path=/usr/local/nginx/logs/access.log \
    --with-pcre \
    --pid-path=/usr/local/nginx/nginx.pid \
    --with-http_ssl_module
```

Las opciones utilizadas han sido:

- `--sbin-path`: path del ejecutable que inicia y para el servidor Nginx.
- `--conf-path`: path del archivo de configuración.
- `--error-log-path`: path del log de error.
- `--http-log-path`: path de logs HTTP del servidor.
- `--with-pcre`: utilizar la librería PCRE del sistema para expresiones regulares.
- `--pid-path`: archivo con el ID del proceso principal.
- `--with-http_ssl_module`: módulo que añadiremos durante la instalación.

##### Compilar configuración

```bash
make
```
##### Instalar el archivo compilado

```bash
sudo make install
```

Revisamos que los archivos utilizados en la configuración existen:

```bash
ls /usr/local/nginx
```

Verificamos versión instalada y la configuración empleada:

```bash
/usr/local/nginx/nginx -V
```

## Módulos

Los módulos amplían las funcionalidades del servidor.

Solo pueden utilizarse de instalarse Nginx mediante `building from sources`.

Hay dos tipos:

- Módulos que vienen en el código de Nginx: ver sección `Modules reference` en [link]<https://nginx.org/en/docs/>.
- Módulos de terceras partes: <https://www.nginx.com/resources/wiki/modules/>

## Cambiar estado del servidor

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
```

[Recursos](https://nginx.org/en/docs/beginners_guide.html)

## Cambiar ruta de los contenidos a mostrar

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

Verificamos que la configuración es correcta:

```bash
sudo nginx -t
```

Tras saber que los cambios son válidos, reiniciamos el servicio `nginx`:

```bash
sudo nginx -s reload
```

Desde el navegador web, visualizamos por ejemplo al archivo que tengamos en `/home/foo/bar/public_html/index.html` accediendo a `http://1.2.3.4./index.html`.

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

