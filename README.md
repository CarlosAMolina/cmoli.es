## Configuration

### Docker

You need to have Docker installed and run it as [rootless](<https://docs.docker.com/engine/security/rootless/>).

### Git

Install [git](<https://git-scm.com/>) to update the project automatically.

### VPS connection

Set in your local host the following environment variables with the VPS configuration and credentials.

Example:

```bash
export VPS_DEV_PORT=123
export VPS_DEV_IDENTITY_FILE=~/.ssh/id_rsa
export VPS_DEV_IP=1.2.3.4
export VPS_DEV_USER=foo
```

To configure the VPS identity file, you can follow this tutorial about how to connect to a server via SSH without credentials <https://cmoli.es/wiki/ssh.html>.

## Run project

Create HTML files and deploy on the VPS:

```bash
cd deploy
make deploy
```

## Test

Test in you local host:

```bash
cd deploy
make test
```
