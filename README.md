[![Build Status](https://api.travis-ci.org/lucasvazq/cushead.svg?branch=master)](https://travis-ci.org/lucasvazq/cushead)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce412113e4144c9f9739a99a0d0b77f5)](https://app.codacy.com/app/lucasvazq/cushead?utm_source=github.com&utm_medium=referral&utm_content=lucasvazq/cushead&utm_campaign=Badge_Grade_Dashboard)
[![codecov](https://codecov.io/gh/lucasvazq/cushead/branch/master/graph/badge.svg)](https://codecov.io/gh/lucasvazq/cushead)
[![PyPI version](https://badge.fury.io/py/cushead.svg)](https://badge.fury.io/py/cushead)

<div align="center">
  <img src="./docs/logo.png" alt="cushead logo">
</div>

# CUSHEAD

**Improve the SEO and the UX of your website.**

**Python Versions:** _>=3.8_

**Package Version**: _\*_

**Status:** _Development_

## Description

Generates a basic structure of the files of a static website, with a main focus
on **SEO** and **UX**.

[View example](./docs/example/)

## Usage

### Example

1. Generate a default config file with images
   `cushead -d -i example/config.json`

2. Read the config file and create all files `cushead -c example/config.json`

### Help

```
usage: cushead { --help | { --config | --default [ --images ] } FILE }

excluding arguments:
  -h, --help     Show this help message and exit.
  -c, --config   Read a config file and create the main files based on it.
  -d, --default  Generate a default config. Can be used with --images.

optional arguments:
  -i, --images   Use with --default. Generate default images that can be used
                 by the default config file. This include: favicon_ico_16px.ico,
                 favicon_png_2688px.png, favicon_svg_scalable.svg and
                 preview_png_600px.png

positional arguments:
  FILE           Input or output file used by --config or --default args.
                 For --config it must be a path to a config file in JSON
                 format. For --default it must be the filename that want to
                 create and add there the default config. If the --images args
                 is setted, the images would be created in the directory of
                 that file.

Examples:
1) Generate default config file with images:
    cushead -d -i config.json
2) Run that config:
    cushead -c config.json
```

## License

**cushead** © 2019 Lucas Vazquez. Released under the
[MIT](http://mit-license.org/) License.
