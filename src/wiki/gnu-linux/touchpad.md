En Arch Linux, cuando touchpad no es detectado, no aparecía la linea `SynPS/2 Synaptics TouchPad`, el resto si se mostraban:

```bash
xinput --list
```

```bash
Virtual core pointer                    	id=2	[master pointer  (3)]
  ↳ Virtual core XTEST pointer              id=4	[slave  pointer  (2)]
  ↳ FOO1234:00 1122:4321                   	id=12	[slave  pointer  (2)]
  ↳ SynPS/2 Synaptics TouchPad              id=14	[slave  pointer  (2)]
Virtual core keyboard                   	id=3	[master keyboard (2)]
  ↳ Virtual core XTEST keyboard             id=5	[slave  keyboard (3)]
  ↳ FOO1234:00 1122:4321 Bar               	id=11	[slave  keyboard (3)]
  ↳ AT Translated Set 2 keyboard            id=13	[slave  keyboard (3)]
```

Ejemplo de logs:

```bash
vi /var/log/Xorg.0.log
```

```bash
[    28.545] (II) config/udev: Adding input device SynPS/2 Synaptics TouchPad (/dev/input/event10)
[    28.545] (**) SynPS/2 Synaptics TouchPad: Applying InputClass "libinput touchpad catchall"
[    28.545] (**) SynPS/2 Synaptics TouchPad: Applying InputClass "touchpad"
[    28.545] (II) Using input driver 'libinput' for 'SynPS/2 Synaptics TouchPad'
[    28.545] (**) SynPS/2 Synaptics TouchPad: always reports core events
[    28.545] (**) Option "Device" "/dev/input/event10"
[    28.548] (II) event10 - SynPS/2 Synaptics TouchPad: is tagged by udev as: Touchpad
[    28.552] (II) event10 - SynPS/2 Synaptics TouchPad: device is a touchpad
[    28.552] (II) event10 - SynPS/2 Synaptics TouchPad: device removed
[    28.595] (**) Option "Tapping" "on"
[    28.596] (**) Option "config_info" "udev:/sys/devices/platform/i8042/serio1/input/input11/event10"
[    28.596] (II) XINPUT: Adding extended input device "SynPS/2 Synaptics TouchPad" (type: TOUCHPAD, id 14)
[    28.600] (**) Option "AccelerationScheme" "none"
[    28.600] (**) SynPS/2 Synaptics TouchPad: (accel) selected scheme none/0
[    28.600] (**) SynPS/2 Synaptics TouchPad: (accel) acceleration factor: 2.000
[    28.600] (**) SynPS/2 Synaptics TouchPad: (accel) acceleration threshold: 4
[    28.602] (II) event10 - SynPS/2 Synaptics TouchPad: is tagged by udev as: Touchpad
[    28.606] (II) event10 - SynPS/2 Synaptics TouchPad: device is a touchpad
[    28.609] (II) config/udev: Adding input device SynPS/2 Synaptics TouchPad (/dev/input/mouse0)
[    28.609] (**) SynPS/2 Synaptics TouchPad: Applying InputClass "touchpad"
[    28.609] (II) Using input driver 'libinput' for 'SynPS/2 Synaptics TouchPad'
[    28.609] (**) SynPS/2 Synaptics TouchPad: always reports core events
[    28.609] (**) Option "Device" "/dev/input/mouse0"
[    28.651] (II) mouse0  - not using input device '/dev/input/mouse0'.
[    28.651] (EE) libinput: SynPS/2 Synaptics TouchPad: Failed to create a device for /dev/input/mouse0
[    28.651] (EE) PreInit returned 2 for "SynPS/2 Synaptics TouchPad"
```

Ejemplo de log cuando hago (verificar si de verdad salen estos logs):

```bash
sudo xinput disable 14
```

```bash
[   224.146] (II) event10 - SynPS/2 Synaptics TouchPad: device removed
```

```bash
sudo xinput enable 14
```

```bash
[   230.953] (II) event10 - SynPS/2 Synaptics TouchPad: is tagged by udev as: Touchpad
[   230.958] (II) event10 - SynPS/2 Synaptics TouchPad: device is a touchpad
```

## Ver relación evento con dispositivo:

```bash
sudo libinput list-devices
```

También se ve en las primeras líneas que muestra `sudo libinput debug-events`

## Mostrar pon pantalla los eventos

Puedes ver que se pulsan las teclas o que se toca el touchpad

```bash
sudo libinput debug-events
```

## Solución

Para que aparezca en `xinput list` tuve que eliminar este archivo `/etc/X11/xorg.conf.d/30-touchpad.conf`.

## Recursos

- Documentación oficial

<https://wiki.archlinux.org/title/Libinput>

- Habilitar y deshabilitar touchpad

<https://askubuntu.com/questions/528293/is-there-a-way-to-restart-the-touchpad-driver>

