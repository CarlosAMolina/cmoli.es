# Neovim plugins

En este apartado veremos cómo instalar varios plugins que suelo utilizar en Neovim.

## Vim-plug

Se trata de un gestor de plugins.

Instalación:

```bash
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```

Para instalar plugins con `vim-plug`, en `~/.config/nvim/init.vim` creamos la sección `call` e indicamos los plugins deseados:

```bash
# vi ~/.config/nvim/init.vim
call plug#begin()
Plug 'neoclide/coc.nvim', {'branch': 'release'}
call plug#end()
```

Tras esto, reiniciamos Neovim y ejecutamos la orden:

```bash
:PlugInstall
```

## Coc

Coc (Conquer of Completion) nos permitirá autocompletar texto.

Es necesario tener instado `nodejs`:

```bash
sudo pacman -S nodejs
```

Instalaremos Coc utilizando el gestor de plugins `vim-plug` (ver sección donde se explica su funcionamiento), añadiendo el plugin `Plug 'neoclide/coc.nvim', {'branch': 'release'}`.

Una vez instalado, al escribir nos aparecerán opciones de autocompletado, pero no podremos seleccionarlas, conviene realizar las siguientes configuraciones en el archivo `~/.config/nvim/init.vim`

- Navegar entre las opciones de autocompletado con el tabulador:

```bash
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"
```

- Seleccionar una opción de autocompletado al pulsar tecla enter:

```bash
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"
```

Para poder instalar plugins mediante `CocInstall`, necesitamos instalar `npm`:

```bash
sudo pacman -S npm
```

## pyright

Para programar en el lenguaje Python, utilizo el plugin `pyright`, puede instalarse utilizando `Coc` (explicado en este apartado de plugins):

```bash
:CocInstall coc-pyright
```

Ahora podremos trabajar con archivos de Python utilizando la ayuda que ofrece `pyright` :).

## Referencias

Coc

<https://github.com/neoclide/coc.nvim>

Pyright

<https://github.com/microsoft/pyright>

Vim-plug

<https://github.com/junegunn/vim-plug#neovim>
