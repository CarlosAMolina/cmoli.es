## Configuration

### Docker

You need to have Docker installed and run it as [rootless](<https://docs.docker.com/engine/security/rootless/>).

### Git

Install [git](<https://git-scm.com/>) to update the project automatically.

## Run project

The media content (images, videos, etc.) must be in the `$HOME/Software/cmoli-media-content` folder using the same paths as the markdown web files. This is required because the media content will be copied from this path to the web content path with the `cp -r` command.

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
