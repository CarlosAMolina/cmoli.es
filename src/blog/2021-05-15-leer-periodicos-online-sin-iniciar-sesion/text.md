# Leer periódicos online sin iniciar sesión

Muchas veces los periódicos online muestran los primeros párrafos de un artículo y, para leerlo entero debemos iniciar sesión o suscribirnos. Esto me ocurrió con el siguiente artículo sobre Signal, una alternativa a WhatsApp enfocada a la privacidad: <https://elpais.com/tecnologia/2021-05-11/como-un-profesor-de-filosofia-en-zamora-colaboro-en-el-desarrollo-de-signal-la-alternativa-de-whatsapp.html>.

![](article-login.png)

> Imagen. Artículo mostrado parcialmente

Por suerte, es posible saltar esta restricción y acceder al contenido del artículo sin necesidad de iniciar sesión, solamente analizando el sitio web.

Para ello, en el navegador web de nuestro ordenador (yo utilizo Firefox, pero cualquier otro también vale), abrimos el menú `Development Tools` pulsando la tecla F12 y elegimos la pestaña `Network`.  Tras esto, recargamos la página web para tener todas las peticiones.

Podemos ver una petición GET que obtiene el HTML del artículo, seleccionando esta petición y accediendo a la sección de `Response`, obtenemos el artículo completo.

![](article-full.png)

> Imagen. Artículo completo

Creo que es un ejemplo sencillo de cómo acceder a información que debería estar oculta. En este caso, lo hemos conseguido analizando el tráfico de red. ¿Valdrá esta técnica en otros artículos y páginas web?

¡Saludos!
