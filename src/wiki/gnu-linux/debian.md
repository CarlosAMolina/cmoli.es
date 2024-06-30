# Debian

## Instalación

Crear usb bootable:

1. Insert usb.
2. Unmount usb.
3. `cp debian.iso /dev/sdX`. Importante, utilizar `sdX`, no `sdX1`.

[Link](https://wiki.debian.org/DebianInstaller/CreateUSBMedia).

## Evitar suspensión al cerrar tapa del portátil

Modificar el siguiente archivo:

```bash
sudo vi /etc/systemd/logind.conf
```

Cambiar:

```bash
#HandleLidSwitch=suspend
#HandleLidSwitchExternalPower=suspend
#HandleLidSwitchDocked=suspend
```

por:

```bash
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

Tras esto, ejecutar:

```bash
sudo service systemd-logind restart
```

### Resouces
<https://unix.stackexchange.com/questions/563729/looking-for-the-settings-that-causes-debian-to-suspend-when-laptop-lid-is-closed>
<https://github.com/systemd/systemd/issues/11638>
<https://superuser.com/questions/1605504/etc-systemd-logind-conf-is-being-ignored>

