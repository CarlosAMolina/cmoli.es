# cmoli.es

## Introducción

La idea de tener una página web, era poder acceder a información que suelo consultar o quisiera compartir con otras personas; de manera que estuviera siempre disponible y fuera sencillo desde cualquier ordenador o móvil.

Inicialmente, utilicé [Blogger](https://www.blogger.com) para escribir pequeños artículos. Con el tiempo quise tener un sitio web más personalizado, pasé a [GitHub Pages](https://docs.github.com/es/pages) y otras soluciones; pero finalmente opté por tener un servidor propio y gestionar todo el contenido e infraestructura. ¿Hay otra opción más entretenida?

Los principales puntos que quería eran:

- HTTPS.
- Dominio propio, y subdominios.
- Escribir en Markdown.
- Contenido estático: HTML, CSS y JS.
- Utilizar imágenes y vídeos.
- Ejecutar software con los mínimos privilegios posibles.

Veamos cómo ha evolucionado la página web y qué software utilicé en cada etapa:

## Primera versión

Los proveedores que contraté, y sigo utilizando, son:

- Para el alojamiento web, opté por un VPS en [Clouding](https://clouding.io/), sistema operativo Debian. La dirección IP está situada en Barcelona, lo que ofrece rápidas respuestas y, comparando con otros proveedores, su opción más básica es muy económica (3,63€/mes, iva incluido). No he tenido problemas con este distribuidor, funciona estupendamente.
- El dominio lo compré en [OVH](https://www.ovhcloud.com/es-es/). Es un dominio .es y actualmente pago al año 8.46€, IVA incluido.

Respecto al software instalado en el servidor y contenido que almacena:

- [Nginx](https://nginx.org/en/). Es el servidor web que ofrece el contenido, respuestas HTTPS y cabeceras que configuré para aumentar la seguridad. No lo instalé con el comando `sudo apt install nginx`, sino que hice un [building from sources](https://cmoli.es/wiki/content/nginx/installation.html); el motivo era trabajar con la última versión de Nginx, tener una instalación más configurada, etc.
- [Certbot](https://certbot.eff.org/). Para crear y renovar los certificados de las conexiones HTTPS. ¿Cómo renovaba el certificado? Manualmente... Sí, cada tres meses tenía una alarma y accedía para ejecutar el comando `sudo certbot certonly --manual`. No podía instalar el plugin de Nginx para renovación automática al haber instalado Nginx haciendo building from sources. La explicación con los pasos puede verse en este [link](https://cmoli.es/wiki/content/nginx/http2.html).
- [Git](https://git-scm.com/). Los archivos Markdown, CSS y JS los guardo en [GitHub](https://github.com/) por lo que descargaba la última versión directamente en el VPS con git.
- Scripts en Bash para generar el contenido web. Estos scripts automatizaban diferentes partes del proceso para que tras iniciarlo, el contenido se generara sin intervención mía.
- Utilizo una nube privada donde tengo las imágenes y vídeos que ofrece el sitio web. Este contenido lo copio al VPS.
- [Docker en modo rootless](https://docs.docker.com/engine/security/rootless/). Para poder ejecutar el programa que desarrollé en Python que, utilizando [Pandoc](https://pandoc.org/MANUAL.html) convierte los archivos Markdown a HTML y copia el contenido multimedia a las rutas a las que apunta el HTML.

### Coste primera versión

En esta primera versión, tuve que contratar en el VPS 10GB en lugar de los 5GB mínimos, lo que incrementó un poco el precio mensual a 4,24€. No recuerdo si también amplié la memoria RAM a 2GB, lo que hubiera elevado el precio a 7,26€.

## Sustituir Nginx y Docker por Go y certificados automáticos

Después de algunos años, quería volver a tener un VPS de 5GB en lugar de los 10GB contratados. Tras hacer limpieza de logs, imágenes Docker de prueba, etc., conseguí bajar a 4,5GB, pero pronto volvería a necesitar más de 5GB.

Los principales cambios fueron:

- Primero, no generar el contenido web en el VPS, sino en mi ordenador y luego subirlo al VPS. Gracias a esto no necesitaba Docker en el VPS; tampoco lo utilizo en local sino que he migrado todo el proceso a Go, [link al proyecto](https://github.com/CarlosAMolina/cmoli.es-deploy); he ganado en velocidad y simplificado el código ya que antes necesitaba, además de Docker, scripts en Python y Bash, los cuales ya estaban siendo un poco complicados de gestionar.
- Aunque Nginx ofrece muchas posibilidades, para compartir contenido web la principal necesidad era HTTPS por lo que pensé en [Caddy](https://caddyserver.com/) que renueva los certificados automáticamente y permite ofrecer mi contenido web; aun así, quise depender lo mínimo posible de programas externos y terminé creando un servidor web en [Go](https://go.dev/) y renovando los certificados con Certbot.
- Finalmente, eliminé la manualidad de renovar los certificados cada tres meses. Antes mencioné que no utilicé Caddy, ayudado por la inteligencia artificial para que me guíe en este proceso, he conseguido tener la renovación automática con Certbot y un pequeño script en Bash; la ventaja de esta solución es que no incremento el almacenamiento necesario instalando software adicional. Resumí los pasos [en este link](https://cmoli.es/wiki/content/certbot/certbot.html)

Sobre Go, estoy encantado de las posibilidades que ofrece.

- Poder generar el binario en local y subirlo al VPS me ahorra instalar software adicional. Este binario ocupa 8,8MB.
- Permite respuestas HTTPS, logs, cabeceras y redireccionamientos que tenía configurados en Nginx. Además, he podido implementar reglas de seguridad, por ejemplo controlar el número máximo de peticiones.

### Coste tras eliminar Nginx y Docker

Gracias a estos cambios, solo he utilizado 2.5GB de almacenamiento; creo que el VPS con la imagen Debian recién instalada ocupaba 2GB.

Por lo que, el coste mensual del VPS vuelve a ser de 3,63€ al mes.
