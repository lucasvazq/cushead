[![Build Status](https://api.travis-ci.org/lucasvazq/cushead.svg?branch=master)](https://travis-ci.org/lucasvazq/cushead)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce412113e4144c9f9739a99a0d0b77f5)](https://app.codacy.com/app/lucasvazq/cushead?utm_source=github.com&utm_medium=referral&utm_content=lucasvazq/cushead&utm_campaign=Badge_Grade_Dashboard)
[![codecov](https://codecov.io/gh/lucasvazq/cushead/branch/master/graph/badge.svg)](https://codecov.io/gh/lucasvazq/cushead)
[![PyPI version](https://badge.fury.io/py/cushead.svg)](https://badge.fury.io/py/cushead)

<div align="center">
  <img src="./docs/logo.png" alt="cushead logo">
</div>

# CUSHEAD

**Improve the SEO and the UX of your website.**

**Python Versions:** _>=3.6, <4.0_

**Package Version**: _*_

**Status:** _Development_

## Description

Generates a basic structure of the files of a static website,
with a main focus on **SEO** and **UX**.

[View example](./docs/example/)


## Usage

### -default --images

`cushead.py -default custom_settings.json --images`

Generate a default config file with images includes

<details>

  <summary>custom_settings.json</summary>

  Can edit all of this settings.

  ```json
{
    "comment":  {
        "About":            "Config file used by python CUSHEAD",
        "Format":           "JSON",
        "Git":              "https://github.com/lucasvazq/cushead",
        "Documentation":    "https://github.com/lucasvazq/cushead/blob/master/README.md"
    },
    "required": {
        "static_url":       "/static/"
    },
    "recommended": {
        "favicon_ico":      "./favicon_ico_16px.ico",
        "favicon_png":      "./favicon_png_1600px.png",
        "favicon_svg":      "./favicon_svg_scalable.svg",
        "preview_png":      "./preview_png_500px.png"
    },
    "default": {
        "general": {
            "content-type":     "text/html; charset=utf-8",
            "X-UA-Compatible":  "ie=edge",
            "viewport":         "width=device-width, initial-scale=1",
            "language":         "en",
            "territory":        "US",
            "clean_url":        "microsoft.com",
            "protocol":         "https://",
            "robots":           "index, follow"
        },
        "basic": {
            "title":            "Microsoft",
            "description":      "Technology Solutions",
            "subject":          "Home Page",
            "keywords":         "Microsoft, Windows",
            "background_color": "#FFFFFF",
            "author":           "Lucas Vazquez"
        },
        "social_media": {
            "facebook_app_id":  "123456",
            "twitter_user_@":   "@Microsoft",
            "twitter_user_id":  "123456"
        }
    },
    "progressive_web_apps": {
        "dir":              "ltr",
        "start_url":        "/",
        "orientation":      "landscape",
        "scope":            "/",
        "display":          "browser",
        "platform":        "web",
        "applications":     [
            {
                "platform":     "play",
                "url":          "https://play.google.com/store/apps/details?id=com.example.app",
                "id":           "com.example.app"
            },
            {
                "platform":     "itunes",
                "url":          "https://itunes.apple.com/app/example-app/id123456"
            }
        ]
    }
}
  ```

</details>

<details>

  <summary>Images</summary>

  ```txt
    favicon_ico_16px.ico
    favicon_png_1600px.png
    favicon_svg_scalable.svg
    preview_png_500px.png
  ```

</details>

### -config

`cushead.py -config custom_settings.json`

Run the script with the custom config generated with -default --images.
This will generate the website structure

<details>

  <summary>List output</summary>

*/: the folder where is the settings json file.

*STATIC/: The statics files folder. It depends on the 'static_url' key in the
settings file.

*IMAGES/: A tons of images files in png format, and one in svg.

```txt
*/
├─ custom_settings.json
└── /output
    ├── index.html
    ├── favicon.ico
    ├── robots.txt
    ├── sitemap.xml
    └── *STATIC/
        ├── manifest.json
        ├── browserconfig.xml
        └── *IMAGES/
```

</details>

## Testing

### Files

[manifest.json](https://manifest-validator.appspot.com/)

[robots.txt](https://sitechecker.pro/es/robots-tester/)

[sitemap.xml](https://www.xml-sitemaps.com/validate-xml-sitemap.html)

### Headers

[Favicons](https://realfavicongenerator.net/favicon_checker)

[Meta-tags](https://www.heymeta.com/)

[Facebook Debugger](https://developers.facebook.com/tools/debug/)

[Twitter Card validator](https://cards-dev.twitter.com/validator)

## Considerations

Here is a list of concepts that comprise good practices to improve **SEO** and
**UX**:

1) Structured data: RDFa, JSON-D, Microdata, GoodRelations, vCard, hCard
2) rel profile attribute for referring to author or website owner
3) ARIA Labels (with role attribute)
4) title attribute to links
5) Maskable icons
6) Accelerated Mobiles Pages
7) Progressive Web Apps
8) Screenshots in manifest for PWA
9) Add PWA to App stores (like the Play Store of Google)
10) Javascript and css minified and purged with short variables names
11) Responsive Design
12) Mobile call and Whatsapp sms for mobiles websites
13) Google my Business integration
14) gzip and bzip2 compression
15) Server Side Rendering
16) Client Side routing
17) HTTP caching in Client Side
18) Content Delivery Network
19) Make svg files scalable
20) [Short and SEO related filenames](https://saradoesseo.com/seo-basics/what-should-i-name-images-for-seo/)
21) svg files must be scalables
22) Think when to use svg instead of img
23) Minimize icon fonts
24) Minify all files (html, css, js, json, xml, images)
25) Purge javascript and css.
26) Obfuscate, if can, css class names and js variablenames
27) Benefit from html5 (`<br>` better than `<br />`)
28) colorblind thinking (keep in mind the color of menus, lines, borders, shadows, and text when are designing website)

## License

**cushead** © 2019 Lucas Vazquez. Released under the [MIT](http://mit-license.org/) License.
