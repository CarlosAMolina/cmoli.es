# Errors

## Contents

- [Install package fails with the requested URL returned error 404](#install-package-fails-with-the-requested-url-returned-error-404)

## Install package fails with the requested URL returned error 404

If you get this error when installing something with `pacman -S`, update and upgrade the system because some old libraries could be deleted from the servers. The system should be restarted after the upgrade.

<https://wiki.archlinux.org/title/System_maintenance#Partial_upgrades_are_unsupported>

```bash
pacman -Syu
```

Try to install the pacakge again.

