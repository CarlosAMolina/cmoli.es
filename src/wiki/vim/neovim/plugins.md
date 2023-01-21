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

### Coc introducción

Coc (Conquer of Completion) nos permitirá autocompletar texto.

### Coc instalación

Es necesario tener instado `nodejs`:

```bash
sudo pacman -S nodejs
```

Instalaremos Coc utilizando el gestor de plugins `vim-plug` (ver sección donde se explica su funcionamiento), añadiendo el plugin `Plug 'neoclide/coc.nvim', {'branch': 'release'}`.

Para poder instalar plugins mediante `CocInstall`, necesitamos instalar `npm`:

```bash
sudo pacman -S npm
```

### Configuración

Una vez instalado, al escribir nos aparecerán opciones de autocompletado, pero no podremos seleccionarlas, conviene modificar el siguiente archivo de configuración para una mejor experiencia y añadir funcionalidades.

```bash
vi ~/.config/nvim/init.vim
```

#### Reducir updatetime

Con esto conseguimos que las acciones se realicen antes, por ejemplo, al resaltar dónde se usa la función sobre la que tengamos el cursor (este resaltado de ejemplo también hay que configurarlo).

```bash
set updatetime=300
```

#### Navegar entre las opciones de autocompletado con el tabulador

```bash
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"
```

#### Seleccionar una opción de autocompletado con la tecla enter

```bash
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"
```

#### Navegar por el código

Debemos estar en el modo comando de Neovim (pulsar escape).

```bash
" GoTo code navigation
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)
```

#### Resaltar código seleccionado

Para resaltar dónde se definió o dónde se utiliza la función, clase, etc sobre la que tengamos el cursor.

```bash
autocmd CursorHold * silent call CocActionAsync('highlight')
```

#### Organizar automáticamente los imports

Desde el modo comando, con `:OR` se organizarán los imports.

```bash
" Add `:OR` command for organize imports of the current buffer
command! -nargs=0 OR   :call     CocActionAsync('runCommand', 'editor.action.organizeImport')
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
