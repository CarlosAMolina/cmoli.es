Nota. Palabras en mayúsculas precedidas por el símbolo $ indica que deben sustituirse por el valor deseado. Ejm: $USER_NAME

## Contenidos

- [Configuración inicial](#configuración-inicial)
- [Crear repositorio remoto desde un repositorio local](#crear-repositorio-remoto-desde-un-repositorio-local)
- [Cambiar nombre de un repositorio](#cambiar-nombre-de-un-repositorio)
  - [GitLab](#gitlab)
- [Staging area](#staging-area)
- [Volver a un commit anterior](#volver-a-un-commit-anterior)
- [Commit](#commit)
  - [Parent commit](#parent-commit)
- [Branches](#branches)
  - [Common ancestor](#common-ancestor)
  - [Merge](#merge)
    - [Target vs source brach](#target-vs-source-brach)
    - [Por qué a veces aparece mensaje de merge y otras no](#por-qué-a-veces-aparece-mensaje-de-merge-y-otras-no)
- [Comandos git](#comandos-git)
  - [cat-file](#cat-file)
- [Continous integration](#continous-integration)
- [SSH](#ssh)
  - [Consideraciones](#consideraciones)
  - [Errores SSH](#errores-ssh)
    - [Error authentication failed](#error-authentication-failed)
    - [Error push permission denied](#error-push-permission-denied)
- [OSINT](#osint)
  - [Email de quién realizó el commit](#email-de-quién-realizó-el-commit)

## Configuración inicial

```bash
git config --global user.name "$USER_NAME"
git config --global user.email $USER_EMAIL
git config --global http.sslVerify false
```

Nota. Indicar que no se verifique el certificado SSL es un error de seguridad, en lugar de añadirlo a la configuración global, puede indicarse cada vez que se utilice el comando git añadiendo alguna de las siguientes opciones:

```bash
git -c http.sslVerify false
```

```bash
git -c http.sslVerify=False
```

## Crear repositorio remoto desde un repositorio local

<https://docs.gitlab.com/ee/gitlab-basics/create-project.html>

<https://georgik.rocks/common-mistake-when-creating-new-git-repo>

<https://docs.gitlab.com/ee/api/namespaces.html>

Paso 1. Hacer un commit local para crear el branch master. Este aparece en .git/config como [branch "master"].

Paso 2. Hacer push. Ejm:

```bash
git push --set-upstream https://$DOMINIO/$USER/$REPOSITORY_NAME.git master
```

## Cambiar nombre de un repositorio

### GitLab

<https://docs.gitlab.com/ee/user/project/settings/>

Ir a configuración del repositorio: https://domain/user/project/edit

Advanced settings > Rename repository: cambiar project name y path.

## Teoría

### Staging area

<https://git-scm.com/about/staging-area>

Subir archivo(s) a la zona de index (staging area):

```bash
# Un archivo.
git add NOMBRE_ARCHIVO

# Todos los archivos.
git add .
```

Subir de la zona de index al repositorio local.

```bash
git commit -m "$MENSAJE_PARA_EL_COMMIT"
```

<img src="https://git-scm.com/images/about/index1@2x.png" alt="" width="300">

## Volver a un commit anterior

<https://stackoverflow.com/questions/4114095/how-to-revert-a-git-repository-to-a-previous-commit/4114122>

```bash
# Al último commit.
git reset --hard HEAD

# A un commit específico.
git reset --hard $COMMIT_ID
```
## Commit

### Parent commit

Como se indica [en este link](https://stackoverflow.com/questions/38239521/what-is-the-parent-of-a-git-commit-how-can-there-be-more-than-one-parent-to-a-g#38239664), el commit padres es el commit (o los commits) en que se basan el commit actual:

- Cuando generas un commit, el commit actual es el padre del nuevo que se genera.
- Cuando mergeas dos commits (mergeo no de tipo fast forward), se genera un nuevo commit cuyos padres son los dos anteriores. Pueden verse con `git log --oneline --graph --parents`.

## Branches

### Common ancestor

El `common ancestor` de dos ramas es el commit más reciente que tienen en común ([link](https://www.freecodecamp.org/news/the-definitive-guide-to-git-merge/)).

Un `common ancestor` `B` es mejor que otro `A` si `B` es más reciente, es decir, si `A` es un `ancestor` de `B`. El `best common ancestor` es el `common ancestor` que no tenga otros `ancestor` mejores que él. Al `best common ancestor` también se le llama `merge base`. [Link documentación](https://git-scm.com/docs/git-merge-base).

Hay situaciones en que haya varios `merge base` (ver ejemplos en la [documentación](https://git-scm.com/docs/git-merge-base#_discussion)).

### Merge

#### Target vs source brach

- Target: la rama en la que te encuentras.
- Source: la rama que indicas en el comando `git merge <branch>`.

#### Por qué a veces aparece mensaje de merge y otras no

Cuando hacemos merge, en caso de que el último commit de una rama sea el best common ancestor de la otra, no habrá un commit message de `Mergeo branch X into Y` porque git únicamente tuvo que hacer un fast forward, no combinó archivos. Esta es la diferencia entre `fast forward merge` y `3 way merge`.

## Comandos git

### cat-file

Permite obtener información de un commit hash. Algunos ejemplos de qué permite:

- Obtener la rama a la que pertenece el commit.
- Analizar los archivos actuales en ese commit y ver su contenido. Por ejemplo con esto podríamos ver el contenido de archivos eliminados.

A continuación, vamos a ver un ejemplo con explicaciones teóricas.

Si ejecutamos el comandos sobre un commit, tenemos:

```bash
$ git cat-file -p b1a7bea
tree 30c0e0197d84a0772d1cb5c0aeb881799bdbd928
parent 6be153f69922aaa141b64880304186f9f3b98b5a
author CarlosAMolina <15368012+CarlosAMolina@users.noreply.github.com> 1715834028 +0200
committer CarlosAMolina <15368012+CarlosAMolina@users.noreply.github.com> 1715834028 +0200

Update wiki git
```

La información mostrada es:

- tree: `tree` indica que se trata de una carpeta.
- parent: id del commit padre al analizado.

Si analizamos `tree` tenemos los archivos y carpetas en ese commit:

```bash
$ git cat-file -p 30c0e01
100644 blob 777be3e2e2b6e8aabd6e817a7e1588b54fe0380a    .gitignore
100644 blob a347037c1839ae4f34a9e3399748fbcdcb2d3de4    CHANGELOG.md
100644 blob b3fbee3f989b71ea85a1d5922c4bebf31fc439d1    LICENSE
100644 blob de6d9dea4245ee0e6ec5365011f7b3d69d945b9f    README.md
040000 tree 8437ea087b6b9727c278e3814e346c1f5737022d    deploy
040000 tree 87ea3d4f0df06354806cb126b8dbf39d87e10aaa    src
```

El término `blob` indica que se trata de un archivo.

Cada commit de git contiene todos los archivos y carpetas en ese momento.

Los 2 primeros caracteres mostrados en el hash de los archivos indica donde se encuentran estos archivo en `.git`. Por ejemplo, para `f7c5a4e5545b761005adc08da8b1efd1499de336` tenemos el archivo:

```bash
.git/objects/f7/c5a4e5545b761005adc08da8b1efd1499de336
```

Si vemos su contenido, será incomprensible, pero podemos verlo con:

```bash
git cat-file -p f7c5a4e5545b761005adc08da8b1efd1499de336
```

Sobre las carpetas con el nombre de los 2 primeros caracteres del hash, he visto que en proyectos con pocos commits, en `.git/object` hay carpetas por cada hash, pero en más grandes no, tal vez se vayan eliminando con el tiempo.

## Continous integration

Ver runner en una máquina:

```bash
ps -ef | grep runner
```

## SSH

El protocolo SSH nos permite ejecutar los comandos de git en el servidor remoto sin tener que indicar nuestro usuario y contraseña.

Los pasos para realizar la configuración pueden consultarse en los siguientes enlaces:

<https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>

<https://docs.gitlab.com/ee/ssh/>

### Consideraciones

Para poder utilizar el protocolo SSH y no introducir nuestras credenciales, el repositorio con el que estemos trabajando debe haberse descargado del siguiente modo:

```bash
git clone git@$SERVIDOR:$USUARO/$REPOSITORIO
# Ejm: git clone git@github.com:CarlosAMolina/cmoli.es
```

### Errores SSH

#### Error authentication failed

En caso de tener error de autenticación al utilizar los comandos de git, puede ser debido a tener activado el doble factor de autenticación; en este caso, hay que utilizar como credenciales un token.

Los pasos para tener este token están explicado en el siguiente enlace:

<https://mycyberuniverse.com/how-fix-fatal-authentication-failed-for-https-github-com.html>

#### Error push permission denied

Si al hacer `push` recibimos el siguiente error:

```bash
ERROR: Permission to URL_REPO.git denied to USER.
fatal: No se pudo leer del repositorio remoto.

Por favor asegúrate de que tengas los permisos de acceso correctos
y que el repositorio exista.
```

Puede ser que nuestro equipo tenga distintos usuarios de git y no estemos utilizando la configuración del usuario con permisos para escribir en el repositorio.

Para solucionarlo, importamos al ssh-agent la clave SSH privada correspondiente al repositorio, por ejemplo:

```bash
ssh-add ~/.ssh/id_ed255190
```

[Referencia](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## OSINT

### Email de quién realizó el commit

Opción 1.

Añadir `.patch` al final del ID del commit. Ejm:

```bash
https://github.com/$USER/$REPOSITORY_NAME/commit/$COMMIT_ID.patch
```

Opción 2.

Buscar el ID del commit:

```bash
https://api.github.com/repos/$USER/$REPOSITORY_NAME/commits
```

Ver info del commit

```bash
https://api.github.com/repos/$USER/$REPOSITORY_NAME/git/commits/$COMMIT_ID
```

Nota. Es posible configurar que se oculte el mail de quien realizó el commit, pero los commits realizados antes de esta configuración seguirán mostrando el email (<https://help.github.com/en/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address>).
