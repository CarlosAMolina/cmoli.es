Installation steps: <https://wiki.archlinux.org/title/Installation_guide>

The following sections show a summary of the required commands.

## Keyboard layout

<https://wiki.archlinux.org/title/Installation_guide#Set_the_keyboard_layout>

```bash
loadkeys es
```

## Check boot mode is efi

```bash
ls /sys/firmware/efi/efivars
```

If the directory is showed, the boot mode is efi.

## Partitions to use

```bash
# Check partitions to use
fdisk -l
# Example, I will use /dev/sda2 which already has an EFI System and /dev/sda6 to install Linux.

# Format the partitions
mkfs.ext4 /dev/sda6

# Mount file systems
mount /dev/sda6 /mnt/
mount --mkdir /dev/sda2 /mnt/boot
```

## Install packages

```bash
pacstrap -K /mnt base linux linux-firmware
```

## Configure the system

Note. With the following method, only Arch will appear in GRUB.

```bash
# fstab
genfstab /mnt >> /mnt/etc/fstab
arch-chroot /mnt
ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime
hwclock --systohc
echo "es_ES.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=es_ES.UTF-8" > /etc/locale.conf
echo "KEYMAP=es" > /etc/vconsole.conf
echo "hpPC" > /etc/hostname
mkinitcpio -P # run only if /etc/mkinitcpio.d/linux.preset does not exist
passwd
pacman -S grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=arch
pacman -S intel-ucode
grub-mkconfig -o /boot/grub/grub.cfg
exit
umount -R /mnt
shutdown -h now
```

Extract the usb before start the system again.

## Start session

Turn on the pc and write `root` as the user, then write you password.

## Configure network

<https://cmoli.es/wiki/gnu-linux/network.html>

## Create non root user

<https://wiki.archlinux.org/title/Users_and_groups#Example_adding_a_user>

```bash
useradd -m x
passwd x
```

## Add non root user to the sudoers file

<https://wiki.archlinux.org/title/Sudo#Using_visudo>

```bash
pacman -S vi
# Add: x   ALL=(ALL:ALL) ALL
```

## Configure GUI

<https://wiki.archlinux.org/title/Xorg>

```bash
pacman -S xorg-server
# Find driver to install
lspci -v | grep -A1 -e VGA -e 3D
# 01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Caicos XT [Radeon HD 7470/8470 / R5 235/310 OEM] (prog-if 00 [VGA controller])
# 	Subsystem: Micro-Star International Co., Ltd. [MSI] Radeon R5 235 OEM
# Radeon HD 7470/8470 -> TeraScale -> ATI (<https://wiki.archlinux.org/title/Xorg#AMD>):
pacman -S xf86-video-ati
# Install display manager
# https://wiki.archlinux.org/title/LightDM
pacman -S lightdm lightdm-gtk-greeter
systemctl enable lightdm
# Configure Xorg keyboard
#<https://wiki.archlinux.org/title/Xorg/Keyboard_configuration#Setting_keyboard_layout>
#<https://wiki.archlinux.org/title/Linux_console/Keyboard_configuration>
localectl --no-convert set-x11-keymap es
localectl status # check x11 is configured
# Install windows manager
# https://wiki.archlinux.org/title/I3
pacman -S i3-wm
pacman -S xfce4-terminal
reboot
# i3lock
pacman -S i3lock
# Configure i3lock in i3 config file adding:
# ```
# bindsym Control+Mod1+l exec i3lock
# ```
# i3 status bar
pacman -S i3status
# Reload i3 with: shift + alt + r
```

### Language packages

In order to be able to write the `~` character, install:

```bash
# This package was installed while installing Firefox.
pacman -S ttf-dejavu
```

### Audio

<https://wiki.archlinux.org/title/Advanced_Linux_Sound_Architecture>

```bash
sudo pacman -S alsa-utils
```

If the sound is muted, you can unmute the Master with:

```bash
alsamixer
# Set `Master` volume for example to 50 by pressing the up arrow key and unmute it by pressing the `m` key.
```

Configure keyboard volume control:

```bash
# Comment lines in ~/.config/i3/config `# Use pactl to adjust volume in PulseAudio.` section and use:
bindsym XF86AudioRaiseVolume exec --no-startup-id amixer set Master 5%+ && $refresh_i3status
bindsym XF86AudioLowerVolume exec --no-startup-id amixer set Master 5%- && $refresh_i3status
bindsym XF86AudioMute exec --no-startup-id amixer set Master toggle && $refresh_i3status
```

## Not done

particion que modificar
```bash
fdisk -l
fdisk /dev/sda
o
n
p
1
<none>
+3.6G
n
e
2
<none>
<none>
n
<none>
+0.5G
n
<none>
<none>
t
6
82
a
1
w
mkswap /dev/sda6
swapon
mkfs.ext4 /dev/sda1

# TODO check wifi encryption (wpa, etc)
pacstrap /mnt base linux linux-firmware vim grub networkmanager dhcpcd netctl wpa_supplicant dialog
```

