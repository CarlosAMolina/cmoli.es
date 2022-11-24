## Redirection 

### Introduction

The user can specify a list of sites where the add-on will apply a redirection automatically to the first iframe/frame source.

If the current tab URL contains any term in the list, it will be redirected to the first iframe/frame URL of the page.

For example, if you visit `https://html.com/tags/iframe/` and scroll down where the iframe `https://www.youtube.com/embed/owsfdh4gxyc` is loaded, if you configured the term `youtube` you will be redirected to that iframe.

You can read a perfect explanation of this option at the following issue:

<https://github.com/CarlosAMolina/checkIframe/issues/1>

### Configuration

Note. If the first iframe/frame URL should not be used as the redirection location, you can add it to the blacklist and will be omitted

The steps to add a term are:

1. Click the `Configuration` button to open the configuration menu.
2. Below `Sources options`, select the `Sites where first source opens automatically` option.
3. Save new terms, you can write them in two ways:
    - One by one

      Write the term in the input box below `New values` and click the `Add` button or press enter in the keyboard.

    - Multiple terms 

      You can write more than one term, each one must be in a different line.

    The saved terms will appear below the input box.

4. Edit saved terms 

    You can edit them by clicking over each saved term and modify the values.

