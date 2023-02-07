## Tipos

- Estáticos: módulos que siempre están cargados.
- Dinámicos: módulos que pueden seleccionarse configurando Nginx.

## Instalación

Es necesario volver a instalar Nnigx especificando en las opciones los módulos deseados.

## Utilizar módulo dinámico

En el archivo de configuración de Nginx, debe utilizarse la directive `load_module` a la que se le pasa la ruta relativa al módulo.
