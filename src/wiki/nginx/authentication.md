## Basic Auth

### Introducción

Permite requerir usuario y contraseña para dar respuesta a peticiones.

### Configuración

Creamos el archivo `.htpasswd`, para ello:

```bash
htpasswd -c /etc/nginx/.htpasswd user_test
```

Del comando anterior:

- `-c`: generar un nuevo archivo.
- `user_test`: nombre del usuario.

Utilizamos la directivas:

- `auth_basic` seguida del mensaje a mostrar.
- `auth_basic_user_file` seguida del archivo de contraseñas.

Ejemplo:

```bash
...
location /secure {
    auth_basic "Secure Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
    try_files $uri $uri/ =404;
}
...
```

Tras introducir las credenciales, si accedemos al recurso de nuevo, no se solicitarán; para que vuelvan a ser pedidas habría que abrir una navegación privada.

