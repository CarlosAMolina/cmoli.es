## Configuration

Before work with the add-on, some steps are required.

### Disable Firefox's pop-up blocker

In order to avoid errors when opening URLs in new tabs, navigate to `about:preferences#privacy` and, under the `Permissions` section uncheck te box next to `Block pop-up windows`.

Source: <https://support.mozilla.org/en-US/kb/pop-blocker-settings-exceptions-troubleshooting#w_pop-up-blocker-settings>

### Rules to modify URLs

The add-on uses regular expressions to deobfuscate and obfuscate the provided URLs.

This means that some characters must be scaped with backslash, for example `.` must be specified as `\.`

These rules must be configured by the user:

1. Click the `Configuration` button and the `Rules configuration` button.
2. Select the rule type to save: deobfuscation or obfuscation.
3. Save new rules to apply, you can write them in two ways:

    - One by one

      This is the default option. You need to complete the `Value to change` and `New value` inputs and click `Add`.

      Example. To change `http://github.com` to `hXXp://github.com`, use `http` as `Value to change` and `hXXp` as `New value`.

    - Multiple rules

      Activate the buttons below `Save more than one rule` and paste the rules. The even rows are the values to change and the odd rules the new values to set.

      Example. To change `http://github.com` to `hXXp[:]//github.com`, paste:

      ```bash
      http
      hXXp
      :
      [:]
      ```
    The saved rules will appear below the input boxes.

4. Edit saved rules

    You can edit them by clicking over each saved rule and modify the values.

#### Deobfuscation rules

To apply these changes:

```bash
hXXp -> http
[:] -> :
[.] -> .
```

You must save the following rules (the `Save more than one rule` option is activated):

```bash
hXXp
http
\[\:\]
:
\[\.\]
.
```

Example. The URL hXXps[:]//github[.]com/CarlosAMolina will be modified to https://github.com/CarlosAMolina.

#### Obfuscation rules

To apply these changes:

```bash
http -> hXXp
: ---> [:]
. ---> [.]
```

You must save the following rules (the `Save more than one rule` option is activated):

```bash
http
hXXp
:
[:]
\.
[.]
```

Example. The URL https://github.com/CarlosAMolina will be modified to hXXps[:]//github[.]com/CarlosAMolina

### Open URLs delay

You can configure a time to wait between each URL oppened by the add-on.

Steps:

1. Click the `Configuration` button at the add-on's popup.
2. Click the `Lazy loading configuration` button and specify the desired milliseconds.
3. Save this value clicking on the `Update` button near the box where you set the desired milliseconds.
