# Neovim

## ¿Qué es?

Neovim es un Fork de Vim con mejoras.

## Instalación

### Arch Linux

```bash
sudo pacman -S neovim
```

## Configuración

### Copiar entre instancias

Para poder copiar entre diferentes instancias de Neovim utilizando `yy` y `pp`, añadir la siguiente línea al archivo de configuración `~/.config/nvim/init.vim`:

```bash
set clipboard+=unnamedplus
```

## Plugins

En este apartado veremos cómo instalar varios plugins que suelo utilizar en Neovim.

### Python

Para programar en el lenguaje Python, utilizo el plugion `pyright`, puede instalarse del siguiente modo:

```bash
```

## Referencias

Arch Linux wiki:

<https://wiki.archlinux.org/title/Neovim>

Clipboard:

<https://neovim.io/doc/user/provider.html#provider-clipboard>

Plugin. Pyright

<https://github.com/microsoft/pyright>
