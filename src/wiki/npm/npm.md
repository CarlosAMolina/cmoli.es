# npm

## Global installation without sudo

To execute commands like `npm install --global web-ext` without sudo, run:

```bash
npm config set prefix '~/.local/'
# Required bash configuration: `export PATH=~/.local/bin/:$PATH`
```

Resources:

- <https://stackoverflow.com/a/59227497>
