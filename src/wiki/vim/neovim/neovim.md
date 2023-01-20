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

Ver [plugins](plugins.html).

## Referencias

Arch Linux wiki:

<https://wiki.archlinux.org/title/Neovim>

Clipboard:

<https://neovim.io/doc/user/provider.html#provider-clipboard>
