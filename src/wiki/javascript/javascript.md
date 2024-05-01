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
