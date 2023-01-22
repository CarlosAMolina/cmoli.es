# Neovim plugins

En este apartado veremos cómo instalar varios plugins que suelo utilizar en Neovim.

## Vim-plug

Se trata de un gestor de plugins.

### Instar Vim-plug

```bash
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```

### Instalar plugins con Vim-plug

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

### Mostrar plugins instalados con Vim-plug

```bash
:PlugStatus
```

### Desinstalar plugins instalados con Vim-plug

Primero, los eliminamos del archivo `init.vim` en la sección `call plug` y ejecutamos:

```bash
:PlugClean
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

#### Coc comandos gestión extensiones

Instalar extensión (ejemplo coc-pyright):

```bash
:CocInstall coc-pyright
```

Mostrar extensiones instaladas:

```bash
:CocList extensions
```

Desinstalar extensión (ejemplo coc-pyright):

```bash
:CocUninstall coc-pyright
```

### Configuración

Una vez instalado, al escribir nos aparecerán opciones de autocompletado, pero no podremos seleccionarlas, conviene modificar el siguiente archivo de configuración para una mejor experiencia y añadir funcionalidades.

Sobre añadir funcionalidades que nos ayuden al editar archivos, para utilizarlas es necesario realizar otras acciones; una opción es instalar extensiones. Por ejemplo, al trabajar con un archivo Python, si queremos ordenar los imports, aunque la opción esté configurada en Coc, debemos instalar la extensión `coc-pyright`.

```bash
vi ~/.config/nvim/init.vim
```

#### Reducir updatetime

Con esto conseguimos que las acciones se realicen antes, por ejemplo, al resaltar dónde se usa la función sobre la que tengamos el cursor (este resaltado de ejemplo también hay que configurarlo).

```bash
" Having longer updatetime (default is 4000 ms = 4s) leads to noticeable
" delays and poor user experience
set updatetime=300
```

#### Navegar entre las opciones de autocompletado con el tabulador

```bash
" Use tab for trigger completion with characters ahead and navigate
" NOTE: There's always complete item selected by default, you may want to enable
" no select by `"suggest.noselect": true` in your configuration file
" NOTE: Use command ':verbose imap <tab>' to make sure tab is not mapped by
" other plugin before putting this into your config
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"
```

#### Seleccionar una opción de autocompletado con la tecla enter

```bash
" Make <CR> to accept selected completion item or notify coc.nvim to format
" <C-g>u breaks current undo, please make your own choice
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
" Highlight the symbol and its references when holding the cursor
autocmd CursorHold * silent call CocActionAsync('highlight')
```

#### Organizar automáticamente los imports

Desde el modo comando, con `:OR` se organizarán los imports.

```bash
" Add `:OR` command for organize imports of the current buffer
command! -nargs=0 OR   :call     CocActionAsync('runCommand', 'editor.action.organizeImport')
```

#### Mostrar comandos disponibles

En modo comando, pulsando la barra espaciadora y la tecla `c`, podremos ver las opciones que permite Coc.

```bash
" Show commands
nnoremap <silent><nowait> <space>c  :<C-u>CocList commands<cr>
```

Podemos movernos por la lista con los cursores de navegación del teclado, seleccionar una opción al pulsar enter y salir de la lista con escape.

Por ejemplo, de tener configurada la opción de organizar los imports, esta saldrá en la lista mostrada por el comando anterior como `editor.action.organizeImport`

## pyright

Para programar en el lenguaje Python, utilizo el plugin `pyright`, puede instalarse utilizando `Coc` (explicado en este apartado de plugins):

```bash
:CocInstall coc-pyright
```

Ahora podremos trabajar con archivos de Python utilizando la ayuda que ofrece `pyright` :).

## Referencias

Coc

- Documentación:

  <https://github.com/neoclide/coc.nvim>

- Comandos gestión extensiones:

  <https://github.com/neoclide/coc.nvim/issues/1311#issuecomment-547225815>

Pyright

<https://github.com/microsoft/pyright>

Vim-plug

<https://github.com/junegunn/vim-plug#neovim>
