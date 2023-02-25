## Tipos

- Estáticos: módulos que siempre están cargados.
- Dinámicos: módulos que pueden seleccionarse configurando Nginx.

## Instalación

Es necesario volver a instalar Nignx especificando en las opciones los módulos deseados.

## Buscar módulos

Por ejemplo, para saber el módulo a instalar para utilizar HTTP2:

```bash
$ ./configure --help | grep http_v2
--with-http_v2_module           enable ngx_http_v2_module
```

## Utilizar módulo dinámico

En el archivo de configuración de Nginx, debe utilizarse la directive `load_module` a la que se le pasa la ruta relativa al módulo.

## Eliminar módulos instalador por defecto

Algunos módulos que se instalan con Nginx no serán utilizados y otros incluso presentan problemas de seguridad, por lo que conviene eliminarlos.

Aquellos que pueden omitirse en la instalación empiezan por `--without`:

```bash
./configure --help | grep without
```

Observando los módulos listados con el comando anterior, buenos candidatos a ser eliminados son:

- `--without-http_autoindex_module`: permite dar respuesta a peticiones sobre el contenido del directorio, lo cual no es recomendable en webs públicas.

Para omitirlos, simplemente los añadimos en la instalación. Ejemplo:

```bash
./configure --without-http_autoindex_module --sbin-path=...
```
