# Neovim

## ¿Qué es?

Neovim es un Fork de Vim con mejoras.

## Instalación

### Arch Linux

```bash
sudo pacman -S neovim
```

## Configuración

La configuración de neovim se realiza en este archivo de configuración:

```bash
vi ~/.config/nvim/init.vim
```

### Copiar entre instancias

Para poder copiar entre diferentes instancias de Neovim utilizando `yy` y `pp`, añadir la siguiente línea al archivo de configuración:

```bash
set clipboard+=unnamedplus
```

### Corrección ortográfica

Para habilitar la corrección ortográfica en Español para solo archivos de tipo Markdown, puede añadirse la siguiente configuración:

```bash
"https://vi.stackexchange.com/questions/6950/how-to-enable-spell-check-for-certain-file-types
augroup markdownSpell
    autocmd!
    autocmd FileType markdown setlocal spell
    autocmd BufRead,BufNewFile *.md setlocal spell
augroup END
set spelllang=es
```

## Plugins

Ver [plugins](plugins.html).

## Referencias

Arch Linux wiki:

<https://wiki.archlinux.org/title/Neovim>

Clipboard:

<https://neovim.io/doc/user/provider.html#provider-clipboard>
