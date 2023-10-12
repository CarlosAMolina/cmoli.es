# USB Linux

## Contents

- [Introduction](#introduction)
- [Work with an USB manually](#work-with-an-usb-manually)
  - [Mount an USB manually](#mount-an-usb-manually)
    - [Mount an USB manually without sudo](#mount-an-usb-manually-without-sudo)
    - [Mount an USB manually with sudo](#mount-an-usb-manually-with-sudo)
  - [Disconnect an USB manually](#disconnect-an-usb-manually)
    - [Unmount an USB manually](#unmount-an-usb-manually)
      - [Unmount an USB manually without sudo](#unmount-an-usb-manually-without-sudo)
      - [Unmount an USB manually with sudo](#unmount-an-usb-manually-with-sudo)
      - [Check unmount an USB manually](#check-unmount-an-usb-manually)
    - [Eject an USB manually](#eject-an-usb-manually)
    - [Power off an USB manually](#power-off-an-usb-manually)
- [Automate work with an USB](#automate-work-with-an-usb)
  - [Configuration](#configuration)
  - [Automate start and end working with an USB](#automate-start-and-end-working-with-an-usb)
  - [Automate notify the USB device](#automate-notify-the-usb-device)
- [FAQ](#faq)
  - [inotify-tools vs udevadm](#inotify-tools-vs-udevadm)
- [Resources](#resources)

## Introduction

When we connect an USB device, we hope to see it on the screen and start working with it. This is how computers work, but not always. What happens if we are using a system that does not take the required actions to mount the USB device? For example, a tiling windows manager like [i3](https://i3wm.org/).

In these cases, we must run the commands to mount the device and, when we want to disconnect it, more commands to unmount and extract the USB are required. This is fine to learn how to work with an USB but repeat this every day is a waste of time.

The aim of [this project](https://github.com/CarlosAMolina/usb-linux) is to automate all the steps to connect and disconnect an USB in a Gnu/Linux system. First, we will see how to do it manually and then, how to automate the process with some scripts that I developed.

I don't want to reinvent the wheel, there are lots of good [projects](https://wiki.archlinux.org/title/Udisks#Mount_helpers) with the same objective. This project was an opportunity to learn Gnu/Linux and Rust.

![](desktop-notification-on.png)

> Image. Desktop USB connection notification

## Work with an USB manually

Some of the following commands require the installation of additional software, see the automated sections to know how to install them.

### Mount an USB manually

A connected USB appears in the `/dev` path starting with `sd`. The part to mount will have the same name ending with a number.

For example, before connect an USB, I have:

```bash
ls /dev/sd*
# /dev/sda  /dev/sda1  /dev/sda2  /dev/sdb
```

After connecting the USB:

```bash
ls /dev/sd*
# /dev/sda  /dev/sda1  /dev/sda2  /dev/sdb  /dev/sdc  /dev/sdc1
```

In this example, the USB is `/dev/sdc` and the part with the data is `/dev/sdc1`.

In order to access de USB data, I have to mount `/dev/sdc1`.

#### Mount an USB manually without sudo

To avoid run sudo commands, we can use the `udisksctl` command, but this won't allow us to set the target path where the device will be mounted:

```bash
udisksctl mount -b /dev/sdb1
# Mounted /dev/sdb1 at /run/media/USER/12345abc-1234-12aa-1a1a-abcdefghijkl
```

#### Mount an USB manually with sudo

To mount an USB in a specific path, for example in `/media/usb`, the `sudo mount` command is required:

```bash
sudo mount /dev/sdc1 /media/usb
```

Now I can work with the USB using the path `/media/usb`:

```bash
ls /media/usb/
# test.txt
```

### Disconnect an USB manually

To disconnect an USB, three steps are required:

- Unmount.
- Eject. Note: maybe this step is not required.
- Power off.

#### Unmount an USB manually

##### Unmount an USB manually without sudo

This can be done with:

```bash
udisksctl unmount -b /dev/sdb1
# Unmounted /dev/sdb1.
```

##### Unmount an USB manually with sudo

We can unmount the part with the USB data (`/dev/sdc1`) or the folder where the USB was mounted (`/media/usb`):

```bash
sudo umount /dev/sdc1
# sudo umount /media/usb # This is valid too.
```

##### Check unmount an USB manually

If we check the `/dev` path, all the devices mentioned previously will appear:

```bash
ls /dev/sd*
# /dev/sda  /dev/sda1  /dev/sda2  /dev/sdb  /dev/sdc  /dev/sdc1
```

Despite that, the path `/media/usb/` won't show the USB data:

```bash
ls /media/usb/
```

Now the USB can be ejected.

#### Eject an USB manually

Note. This step can be omitted, I think it isn't required thanks to the `power-off` option that we will run in the next section.

The path to eject is the USB raw device, in this example it's value is `/dev/sdc`:

```bash
sudo eject /dev/sdc
```

At this point, the part with the data, `/dev/sdc1`, won't appear:

```bash
ls /dev/sd*
/dev/sda  /dev/sda1  /dev/sda2  /dev/sdb  /dev/sdc
```

Before disconnect the USB, it must be powered off.

#### Power off an USB manually

The last step before disconnect an USB is to power off it. If we omit this point, the USB can be damaged.

We run the following command over the raw device:

```bash
udisksctl power-off -b /dev/sdc
```

No USB folder will remain in `/dev`:

```bash
ls /dev/sd*
# /dev/sda  /dev/sda1  /dev/sda2  /dev/sdb
```

If the USB has a light, it will be turned off.

## Automate work with an USB

The USB mount and unmount processes has been automated in the project [usb-linux](https://github.com/carlosamolina/usb-linux). Let's see how to configure it!

### Configuration

First, install and configure the required software:

- [Dunst](https://wiki.archlinux.org/title/Dunst#Installation)
- [libnotify-bin](https://packages.debian.org/sid/libnotify-bin)
- [Rust](https://www.rust-lang.org/tools/install)
- [udisks2](https://wiki.archlinux.org/title/Udisks#Installation)

To configure Dunst, for example in [i3](https://i3wm.org/), add the following line to the `~/.config/i3/config` file (you can check my [dotfiles](https://github.com/CarlosAMolina/dotfiles/blob/main/dotfiles/config/i3/config)):

```bash
exec --no-startup-id dunst
```

Download the [project](https://github.com/CarlosAMolina/usb-linux) and build the Rust package:

```bash
cd ~/Software/
git clone git@github.com:carlosamolina/usb-linux
cd ~/Software/usb-linux/src/usb/
cargo test # Check the tests pass.
cargo build
```

Add a symlink to the binary to run it with the `usb` command:

```bash
sudo ln -s $HOME/Software/usb-linux/src/usb/target/debug/usb /usr/local/bin/usb
```

### Automate start and end working with an USB

Now, the manual steps to start or end an USB can be done with these commands:

```bash
usb /dev/sdc1 on # Mount an USB.
usb /dev/sdc1 off # Unmount, eject and power-off an USB.
```

With this configuration, some manual steps are avoided but we still need the USB device's name. Let's configure a notification that will give us this value.

### Automate notify the USB device

In order to know the name given to the USB device, in [i3](https://i3wm.org/), add the following line to the `~/.config/i3/config` file (you can check my [dotfiles](https://github.com/CarlosAMolina/dotfiles/blob/main/dotfiles/config/i3/config):

```bash
exec --no-startup-id $HOME/Software/usb-linux/src/bash/monitor
```

The previous script will monitor new USB devices and call the Rust binary to show a notification with the device's name and automatically mount the device, the notification will show the mounted path too.

![](notification-on.png)

> Image. USB connection notification

## FAQ

### inotify-tools vs udevadm

The first approach to monitor when a new device is connected was to use [inotify-tools](https://github.com/inotify-tools/inotify-tools) pointing to the `/dev` path, but it raises an error if the USB is mounted automatically after being detected.

The error is [Error looking up object for device](https://github.com/storaged-project/udisks/issues/711) and is avoided using `udevadm` as the [Arch Linux wiki shows](https://wiki.archlinux.org/title/Udisks#udevadm_monitor).


## Resources

- Project: <https://github.com/CarlosAMolina/usb-linux>
