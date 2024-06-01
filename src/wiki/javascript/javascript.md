## Configure the project development environment

### eslint

#### Install and configuration

In the main path of the project run the following command and answer the questions:

```bash
npm init @eslint/config
```

A file like `.eslintrc.json` or `eslint.config.js` has been created.

#### Work with eslint

Show help:

```bash
npx eslint --help
```

Run eslint over all files to show problems in the code:

```bash
npx eslint .
```

Avoid using `npx` and use `npm instead`. Modify `package.jon` file:

```json
   "scripts": {
     "lint": "eslint .",
```

Run using npm:

```bash
npm run lint
```

## Modules

### Open js code with modules in the browser

This is not possible, [as MDN describes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules#troubleshooting):

> If you try to load the HTML file locally (i.e. with a file:// URL), you'll run into CORS errors due to JavaScript module security requirements. You need to do your testing through a server. GitHub pages is ideal as it also serves .mjs files with the correct MIME type.

Solution, we can open the html using a server like [http-server](https://www.npmjs.com/package/http-server):

```bash
npm install http-server --save-dev
npm exec http-server
firefox http://127.0.0.1:8080
```
