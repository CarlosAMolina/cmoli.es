# Neovim

## Contenidos

- [Introducción Neovim](#introducción-neovim)
- [Instalación](#instalación)
  - [Arch Linux](#arch-linux)
- [Configuración](#configuración)
  - [Copiar entre instancias](#copiar-entre-instancias)
  - [Corrección ortográfica](#corrección-ortográfica)
    - [Errores corrección ortográfica](#errores-corrección-ortográfica)
      - [No encuentra archivo](#no-encuentra-archivo)
- [Plugins](#plugins)
- [Referencias](#referencias)

## Introducción Neovim

Neovim es un fork de Vim con mejoras.

## Instalación

### Arch Linux

```bash
sudo pacman -S neovim
```

## Configuración

La configuración de Neovim se realiza en el siguiente archivo:

```bash
vi ~/.config/nvim/init.vim
```

### Copiar entre instancias

Para poder copiar entre diferentes instancias de Neovim utilizando `yy` y `pp`, añadir la siguiente línea al archivo de configuración:

```bash
set clipboard+=unnamedplus
```

### Corrección ortográfica

Habilitamos la corrección ortográfica en español para solo archivos de tipo Markdown con la siguiente configuración:

```bash
augroup markdownSpell
    autocmd!
    autocmd FileType markdown setlocal spell
    autocmd BufRead,BufNewFile *.md setlocal spell
augroup END
set spelllang=es
```

#### Errores corrección ortográfica

##### No encuentra archivo

De tener este error al iniciar Neovim:

```bash
Warning: Cannot find word list "en.utf-8.spl" or "en.ascii.spl"
Warning: Cannot find word list "en.utf-8.spl" or "en.ascii.spl"
```

La solución es:

```bash
ln -s .vimrc .nvimrc
ln -s .vim .nvim
```

## Plugins

Ver [plugins](plugins.html).

## Referencias

Arch Linux wiki

<https://wiki.archlinux.org/title/Neovim>

Clipboard

<https://neovim.io/doc/user/provider.html#provider-clipboard>

Corrección ortográfica

  - Habilitar para ciertos archivos

    <https://vi.stackexchange.com/questions/6950/how-to-enable-spell-check-for-certain-file-types>

  - Error no encontrar archivo

    <https://github.com/neovim/neovim/issues/1551#issuecomment-64467321>
