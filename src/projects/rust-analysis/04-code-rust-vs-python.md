# Código Rust vs Python

## Introducción 

Iniciamos con esta entrada las comparaciones entre Rust y Python. 

Observaremos partes del código para mostrar las similitudes y diferencias en el programa desarrollado en estos dos lenguajes.

## Partes del programa

En ambos lenguajes, el programa está organizado en los mismos módulos para que sea sencillo compararlos:

```bash
$ tree python/
python/
├── pyproject.toml
├── requirements-dev.txt
├── src
│   ├── create_file.py
│   ├── filter_file.py
│   ├── lib.py
│   ├── main.py
│   ├── m_log.py
│   ├── read_file.py
│   └── write_file.py
└── tests
    └── unit
        ├── __init__.py
        ├── test_filter_file.py
        └── test_m_log.py

$ tree rust
rust
├── Cargo.lock
├── Cargo.toml
└── src
    ├── create_file.rs
    ├── filter_file.rs
    ├── lib.rs
    ├── main.rs
    ├── m_log.rs
    ├── read_file.rs
    └── write_file.rs
```

Exceptuando los archivos de configuración propios de un proyecto en Python o Rust, la carpeta `src` con el código del programa muestra que ambos proyectos tienen los mismos archivos.

Otra diferencia es la parte de los tests, en Python tienen su propia carpeta y en Rust están escritos dentro de los archivos con el código del programa.

A continuación, se describe la función de cada parte y algunos ejemplos de similitudes y diferencias entre Python Y Rust.

### Recibir los valores dados por el usuario

Lo primero a realizar por el programa es recibir por línea de comandos los valores introducidos por el usuario. El único input necesario es el path donde están los archivos de logs a convertir.

En los siguientes ejemplos puede verse cómo librerías que vienen incorporadas por defecto en Python, permiten escribir esta parte de una manera sencilla, es decir, guarda los valores recibidos del usuario y ofrece mensajes de ayuda sin tener que implementarlo nosotros, en cambio, sí hay que escribir esto en Rust de no utilizar librerías externas.

- Rust

El archivo `main.rs` lee la entrada del usuario con el módulo `std::env`:

```rust
use std::env;

....

    let config = Config::new(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });
```

En el archivo `lib.rs` vemos cómo se lee y guarda la entrada del usuario en una estructura `Config`:

```rust
pub struct Config {
    pathname: String,
}

impl Config {
    pub fn new(mut args: env::Args) -> Result<Config, &'static str> {
        //println!("Arguments: {:?}", args);
        args.next();
        let pathname = match args.next() {
            Some(arg) => arg,
            None => return Err("No pathname provided"),
        };
        Ok(Config { pathname })
    }
}
```

- Python

En Python, para leer argumentos y generar mensajes de ayuda, se utilizó la líbrería `argparse`:

```python
import argparse

...

def get_args_parsed():
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    parser = argparse.ArgumentParser(description="Export Nginx logs to a csv file.")
    parser.add_argument(
        "pathname",
        type=str,
        help="path to a folder with the log files or to an specific file",
    )
    return parser.parse_args()
```

### Ordenar archivos de logs a analizar

Una vez se conoce la ruta con los archivos a analizar, deben ordenarse desde el más antiguo hasta el más actual. Esto es necesario para que el archivo `csv` final tenga los logs ordenados cronológicamente.

### Modificar logs

Al leer los logs, debe separarse con comas cada parte (dirección IP, paths solicitados, códigos de respuesta, etc) para generar el archivo .csv final.

### Programa principal

Todas las partes anteriores se orquestan en la función `run()`.

La organización del código es similar en ambos lenguajes:

- Rust

```rust
pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    println!("Checking: {}", &config.pathname);
    let (mut writer_csv, mut writer_error) = create_file::get_result_writers(&config.pathname)?;
    for pathname in filter_file::get_pathnames_to_analyze(&config.pathname)? {
        for line in read_file::get_lines_in_pathname(&pathname) {
            let line_str = line.expect("Something went wrong reading the line");
            let log = m_log::get_log(&line_str);
            match log {
                None => {
                    write_file::write_to_file_error(line_str, &mut writer_error)?;
                }
                Some(log_csv) => {
                    write_file::write_to_file_result(log_csv, &mut writer_csv)?;
                }
            }
        }
    }
    writer_csv.flush()?;
    Ok(())
}
```

- Python

```python
def run(args):
    print(f"Checking: {args.pathname}")
    pathname_csv, pathname_error = create_file.get_pathnames_to_work_with(args.pathname)
    with open(pathname_csv, "w") as file_csv, open(pathname_error, "w") as file_error:
        writer_csv = create_file.get_csv_writer(file_csv)
        writer_csv.writeheader()
        for pathname in FilenamesFilter().get_pathnames_to_analyze(args.pathname):
            for line in FileReader().get_lines_in_pathname(pathname):
                if len(line) != 0:
                    log = m_log.get_log(line)
                    if log is None:
                        write_file.write_to_file_error(line, file_error)
                    else:
                        write_file.write_to_file_result(log, writer_csv)
```

## Conclusión

Con lo visto en los ejemplos anteriores, extraemos las siguientes conclusiones:

- El código en Python es más sencillo de leer que Rust; la sintaxis de Rust puede resultar más compleja.
- Python ofrece por defecto módulos con muchas opciones ya implementadas mientras que en Rust hemos de escribirlo nosotros. Por ejemplo, al interactuar con valores que introduzca el usuario por terminal, con Python ya hay soluciones que detectan y guardar los valores, permiten configurar mensajes de ayuda para los argumentos, configurarlos como obligatorios u opcionales, etc.

## Recursos

Programa que convierte archivos de logs en `csv`:

<https://github.com/CarlosAMolina/nginx-logs>

## Links de este tutorial

- [Página principal](introduction.html).

