# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - TODO
### Added
- Toc to the project Rust VS other languages.
- Add more sections to the project Rust VS other languages.

## [0.14.0] - 2023-03-10
### Fix
- Deploy: detect if the current branch is updated fails if the origin branch was updated from a different path that the current project path.

### Changed
- Deploy: exit if git branch didn't have the remote changes for makefile instead of for all files.

### Removed
- Deploy: the first thing to do is to update the git branch.

## [0.13.0] - 2023-03-08
### Added
- Deploy:
  - Wait until Docker commands can be executed.
  - Exit if git branch didn't have all the remote changes.

### Changed
- Deploy:
  - The first thing to do is to update the git branch.
  - Move update git branch to its own script file.

## [0.12.0] - 2023-03-07
### Added
- Deploy: test with custon Nginx config files.
- Custom error pages.
- UFC: weight introduction.
- Wiki Nginx: added more information.
- Wiki Neovim: add Pyright config to avoid reportMissingImports error.
- Wiki Gnu/Linux:
  - Arch Linux installation steps.
  - Partitions.

### Changed
- Wiki vi: change Vim to Vi in index.html and separate Vim and Neovim.
- Image files are now stored locally instead of being requested from AWS S3.
- Media content is retrieved from an external folder when the docker volume is created.

### Removed
- Image files.
- Deploy: send files to the VPS.

## [0.11.3] - 2023-03-05
### Fix
- Felices fiestas video meta image for Linkedin.

## [0.11.2] - 2023-02-10
### Added
- Wiki terminal: st.

## [0.11.1] - 2023-01-25
### Added
- Wiki Neovim: fix spell errors.
- Wiki Git: fix push permission denied.

### Changed
- Move wiki ssh file to its own folder.

## [0.11.0] - 2023-01-22
### Added
- Wiki Neovim.

## [0.10.2] - 2023-01-15
### Changed
- Improve ssh contents.
- Wiki git clone URL example.

### Fix
- VPS connection using identity file.

## [0.10.1] - 2023-01-02
### Changed
- Open github.com in the same tab instead of in a new one.

## [0.10.0] - 2022-12-26
### Added
- Wiki Gnu-Linux TouchPad.
- Deploy, activate Docker service if not active.

### Changed
- Section no informatica, ufc: add no hover table th rowspan.
- Deploy:
    - Script remove-volumes: accept array of arguments and raise exception if the volume could not be removed.
    - Stop container: raise exception if the container has not been stopped.
    - Create pandoc script: wait until the container ends and raise exception if the script has not been created.
    - Convert md to html: wait until the container ends.
    - Create Nginx server: wait until Ningx server is listening.
    - Refactor pass some values as arguments.

### Fixed
- Flexbox social icon in main page to avoid reversed focus when there is more than one icon.

## [0.9.2] - 2022-12-08
### Added
- Project Rust Analysis. Some sections.

## [0.9.1] - 2022-12-05
### Added
- UFC weight converter.
- UFC responsive table.

### Changed
- Move common settings to base.css.

## [0.9.0] - 2022-11-27
### Added
- No computing section.

## [0.8.0] - 2022-11-27
### Added
- Nginx Docker for local testing.

### Changed
- Do not use `src` in the path of the volume with the web content.
- Rename some variables.

## [0.7.1] - 2022-11-27
### Added
- base.css file with common css configuration.

## [0.7.0] - 2022-11-22
### Added
- Wiki pages. GitHub Pages migration is completed.

### Removed
- GitHub Pages icon.

## [0.6.0] - 2022-11-20
### Added
- Projects pages:
  - Check Iframe.
  - Requests Custom.
  - USB Linux.
  - Work With URLs.

### Changed
- The home icon now loads the linked URL in the current browsing context.

## [0.5.0] - 2022-11-14
### Changed
- Move deploy logic to the `deploy` folder.
- Use Docker containers to:
  - Create the Pandoc script that converts md files to html.
  - Convert md files to html.

## [0.4.0] - 2022-10-31
### Added
- Python script to detect the Markdown files to convert to HTML.

### Changed
- Makefile: convert Markdown to HTML using the added Python script.

## [0.3.0] - 2022-10-12
### Added
- Pandoc template: header with home icon.

## [0.2.0] - 2022-10-09
### Added
- Makefile: convert Markdown to HTML and deploy on the VPS.
- Blog independent of GitHub Pages.
- Wiki entry independent of GitHub Pages.

## [0.1.0] - 2022-08-16
### Added
- Index page.
- Felices Fiestas page.

