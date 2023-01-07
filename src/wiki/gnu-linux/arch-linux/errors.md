# Errors

## Install package with pacman -S. The requested URL returned error 404

Update and upgrade the system because some old libraries could be deleted from the servers. The system should be restarted after the upgrade.

<https://wiki.archlinux.org/title/System_maintenance#Partial_upgrades_are_unsupported>

```bash
pacman -Syu
```

Try to install the pacakge again.

