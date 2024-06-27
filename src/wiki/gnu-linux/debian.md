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

Cambiar `#HandleLidSwitch=suspend` por `#HandleLidSwitch=ignore`.

Tras esto, ejecutar:

```bash
sudo service systemd-logind restart
```

[Link](https://unix.stackexchange.com/questions/563729/looking-for-the-settings-that-causes-debian-to-suspend-when-laptop-lid-is-closed)

