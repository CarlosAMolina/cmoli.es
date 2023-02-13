# Testing

## Apache Benchmark

Sirve para conocer el comportamiento del servidor al responder a las peticiones.

Documentación en el siguiente [link](https://httpd.apache.org/docs/2.4/programs/ab.html).

Ejemplo, para enviar 100 peticiones, 10 concurrentes:

```bash
ab -n 100 -c 10 http://localhost
```

De los resultados del anterior comando, destacar los `Request per second` y `Time per request`, este último es el tiempo medio en recibir respuesta para una petición.

