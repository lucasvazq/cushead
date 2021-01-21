[![Build Status](https://api.travis-ci.org/lucasvazq/cushead.svg?branch=master)](https://travis-ci.org/lucasvazq/cushead)
[![codecov](https://codecov.io/gh/lucasvazq/cushead/branch/master/graph/badge.svg)](https://codecov.io/gh/lucasvazq/cushead)
[![PyPI version](https://badge.fury.io/py/cushead.svg)](https://badge.fury.io/py/cushead)

<div align="center">
  <img src="https://github.com/lucasvazq/cushead/raw/master/docs/logo.png" alt="cushead logo">
</div>

# CUSHEAD

**Generates a basic website template with a focus on _SEO_ and _UX_.**

## Description

This is a small script that allows you to generate a basic template of a website through a configuration file.\
In this file, you can define different variables that will produce a different template in each case.

[View live example](https://lucasvazq.github.io/cushead/)\
[View example of generated files](https://github.com/lucasvazq/cushead/blob/master/docs/examples/relative_static_url/example/output)

## Installation

`pip install cushead`

_Required python version >= 3.8_

## Usage

```
usage: cushead { --help | { --config | --default [ --images ] } FILE }

excluding arguments:
  -h, --help     Show this help message and exit.
  -c, --config   Read a config file and create the website template based on it.
  -d, --default  Generate a default config. Can be used with --images.

optional arguments:
  -i, --images   Use with --default. Generate default images that can be used by the default config file.
                 This include: favicon_ico_16px.ico, favicon_png_2688px.png, favicon_svg_scalable.svg and preview_png_600px.png

positional arguments:
  FILE           Input or output file used by the --config or --default arguments.
                 For --config it must be a path to a config file in JSON format.
                 For --default it must be the destination path where to want to create the default config.
                 If the --images argument is set, the images would be created in the directory of that file.

Examples:
1) Generate default config file with images:
  cushead --default --images config.json
2) Run that config:
  cushead --config config.json
```

## Recomendation

Web development is an area that is very evolved today. It has grown a lot over the years and, like everything that proliferates, it has become more complex.
This little package only solves a small part of all the problems that exist in the field of web development. If you want to take a closer look, here is an interactive website that shows a lot of things to consider when working in this area: [andreasbm/web-skills][web-skills]\
My advice is don't get stuck with so much information, the sites will work anyway. Only if the expense is justified, it is always good to face all these things with a team and try to use already created tools that are kept up to date.

[web-skills]: https://andreasbm.github.io/web-skills/

## License

cushead © 2019 Lucas Vazquez. Released under the [MIT][license] License.

[license]: http://mit-license.org/
