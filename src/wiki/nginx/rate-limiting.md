# Rate limiting

## Introducción

Controlar el número de peticiones que el servidor puede responder y cómo hacerlo ofrece:

- Seguridad. Por ejemplo contra ataques de fuerza bruta.
- Reliability. Protege el servidor contra picos de peticiones.
- Permite controlar la prioridad de las peticiones.

## Configuración

El limit zone se define en el context `http` y luego se utiliza en otros context de manera mas específica (`server`, `location`, etc).

Se define el limit zone con la directiva `limit_req_zone` y las siguientes configuraciones:

- En qué fijarse para aplicar el rate limiting:

    - `$server_name`: aplicarlo a peticiones en base al nombre del servidor, es decir sobre todo lo que haya en la directiva `server`.
    - `$binary_remote_addr`: aplicarlo según la IP del cliente que se conecta al servidor. Es útil en páginas de login para evitar ataques de fuerza bruta desde una misma IP.
    - `$request_uri`: sin importar el cliente, se fija en la URI solicitada. De recibir esta más peticiones de las configuradas, aplicará las limitaciones.

- Nombre del limit zone.
- Tamaño del limit zone en memoria. Es definido tras el nombre y dos puntos.
- Frecuencia de peticiones por unidad de tiempo que no pueden excederse. Por ejemplo, `60r/m` indica 60 peticiones por minuto, una por segundo, por lo que es lo mismo a `1r/s`. Indica la frecuencia de peticiones por la unidad de tiempo, no el número de peticiones; es decir, continuando con el ejemplo anterior, no significa que pueda aceptar máximo 60 peticiones en 1 minuto y tener que esperar al siguiente para seguir aceptando, sino que solo puede aceptar 1 petición por segundo.

Ejemplo de configuración en la que solo permitir 1 petición por segundo:

```bash
http {
    ...
    # Define limit zone
    limit_req_zone $request_uri zone=MYZONE:10m rate=1r/s;

    server {
        ...
        location = /rate-limiting.txt {
            limit_req_zone=MYZONE;
            ...
        }
    }
}
```

Para probarlo, con el siguiente test enviaremos 10 peticiones en menos de 1 segundo (2 tandas de 5 peticiones a la vez en cada una) por lo que solo tendrá respuesta la primera de las 10 peticiones.

```bash
siege -v -r 2 -c 5 https://localhost:8080/rate-limiting.txt
```

También podemos verificando al pedir las cabeceras, si lo hacemos en menos de un segundo, obtendremos un error 503 Service Unavailable:

```bash
curl -Ik https://localhost:8080/rate-limiting.txt
```

## Enlaces

- Artículo Nginx

<https://www.nginx.com/blog/rate-limiting-nginx/>

- Artículo freeCodeCamp

<https://www.freecodecamp.org/news/nginx-rate-limiting-in-a-nutshell-128fe9e0126c>
