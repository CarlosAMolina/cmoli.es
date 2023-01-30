# Nginx configuración

Tras modificar la configuración de Nginx, es necesario verificar que es correcta (ver apartado con los comandos) y reiniar el servicio `nginx`.

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

#### Contexts más importantes

- http: configura lo relacionado con HTTP.
- server: donde definimos un host virtual.
- location: para gestionar/buscar términos en las peticiones que recibe el servidor.

### Directive

Son opciones de configuración específicas utilizadas en los archivos, formados por un nombre y un valor. Por ejemplo:

```bash
server_name foo.com;
```

En el `main context` configuramos `directives` globales que aplican a todos los procesos.

La lista de directives puede verse en este [link](https://nginx.org/en/docs/dirindex.html).

## Editar archivo `nginx.conf`

En esta sección veremos cómo editar el archivo `nginx.conf`, podemos borrar todo su contenido e ir añadiendo lo que veremos a continuación, donde se describe cómo configurar cada context.

### Context events

Aunque esté vacío, es necesario dejarlo en el archivo para tener una configuración válida:

```bash
event {}
```

### Context http

#### Context types o directive include

De no tener este directive, Nginx no enviará los archivos `.css` con la cabecera con el MIME type correcto, sino como `Content-Type: text/plain`, puede verificarse haciendo una petición a las cabeceras del archivo:

```bash
curl -I http://1.2.3.4./style.css
```

Se soluciona definiendo el content type para cada extensión de archivos mediante:

```bash
types {
    text/html html
    text/css css;
}
```

En lugar de escribir todos los casos manualmente, puede cargarse el archivo `mime.types` con la directive `include`:

```bash
include mime.types
```

Este archivo posee los content type para diferentes extensiones de archivos y se define utilizando la ruta relativa a `nginx.conf`, en este casos ambos archivos se encuentran en la misma ruta.


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

Configura el dominio, sudominio o IP para el que aplica el context `server`.

Puede aceptar wildcards como el asterisco, por ejemplo `*.foo.com` aceptará conexiones de cualquier subdominio, como `www.foo.com`, `images.foo.com`, etc.

##### Directive `root`

Es el `path` principal desde el que Nginx gestionará las peticiones.

Por ejemplo, de recibir la petición `/images/dog.png`, Nginx buscará en `/home/foo/bar/public_html/images/dog.png`.

Desde el navegador web, visualizamos por ejemplo al archivo que tengamos en `/home/foo/bar/public_html/images/dog.png` accediendo a `http://1.2.3.4./images/dog.png`.

[Recursos](https://www.nginx.com/blog/setting-up-nginx/)

##### Location blocks

El context `location` sirve para interceptar una petición y ofrece alguna respuesta, por ejemplo una redirección, devolver un string, etc.

Tras `location` se indica el prefix match de ser necesario (lo veremos a continuación) y la URI a interceptar

Hay diferentes modos, cada cual tiene mayor prioridad que el resto, es decir, se ejecutará aunque los otros estén escritos antes en la configuración. De mayor a menor orden de prioridad son:

- Exact match.
- Preferencial prefix match.
- Regex match.
- Prefix match.

###### Exact match

Utiliza el símbolo `=` como el match modifier. Ofrece la respuesta de solicitar específicamente esa URI.

```bash
location = /greet {
    return 200 'Hi from "/greet" location.';
}
```

La URL que obtendrá la respuesta es:

- http://1.2.3.4/greet

###### Preferencial prefix match

Es igual que `prefix match` pero se configura utilizando `^~` y tiene mayor prioridad que el `regex math`.

```bash
location ^~ /greet {
    return 200 'Hi from "/greet" location.';
}
```

###### Regex match

Añadiendo el símbolo `~` como el match modifier, ofreceremos la respuesta de solicitar lo que concuerde con la expresión regular especificada.

Importante, es sensible a mayúsculas y minúsculas, para hacerlo case insensitive, utilizamos `~*`.

Por ejemplo, para responder a `/greet`, case insensitive, seguido de cualquier número del 0 al 9:

```bash
location ~* /greet[0-9] {
    return 200 'Hi from "/greet" location.';
}
```

###### Prefix match

En el siguiente ejemplo, todo lo que empiece por `/greet` devolverá la respuesta indicada.

```bash
location /greet {
    return 200 'Hi from "/greet" location.';
}
```

Ejemplo de URLs que devolverán esa respuesta:

- http://1.2.3.4/greet
- http://1.2.3.4/greeting/foo

## Variables

Nginx tiene 2 tipos de variables:

### Variables propias de Nginx

Ejemplo: `$http`, `$uri`, `$args`.

La lista de variables de Nginx puede verse en este [link](https://nginx.org/en/docs/varindex.html); entre paréntesis se indica el módulo que permite utilizarlas.

Ejemplo uso en un string:

```bash
location /whoami {
    return 200 "$host\n$uri\n$args\nName: $arg_name";
}
```

Visitar la URL "http://1.2.3.4/whoami?name=foo" devolverá:

```bash
2.8.2.1
/whoami
name=foo
Name: foo
```

Se observa cómo con `arg_...` podemos acceder al valor de los argumentos.

### Variables que podemos definir

Se definen indicando su nombre (iniciado con símbolo dolar) y luego el valor.

Pueden ser de tipo:

- Booleano.
- String.
- Números enteros.

Ejemplo:

```bash
set $is_holiday true;
set $user_name 'foo';
set $min_age 18;
```

## Conditionals or If statements

No deben usarse dentro de los context `location` ya que provocan comportamientos inesperados, mas información en el [link](https://www.nginx.com/resources/wiki/start/topics/depth/ifisevil/).

Ejemplo para devolver pantalla de error de no incorporar el API Key correcto en la petición:

```bash
if ( $arg_apikey != 123 ) {
    return 401 "Incorrect API Key";
}

location ...
```

Pueden utilizarse expresiones regulares con `~`. Ejemplo:

```bash
set $weekend 'No';

if ( $date_local ~ 'Saturday|Sunday' ) {
    set $weekend 'Yes';
}

location /is_weekend {
    return 200 $weekend
}
```

