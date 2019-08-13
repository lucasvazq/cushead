[![Build Status](https://api.travis-ci.org/lucasvazq/cushead.py.svg?branch=master)](https://travis-ci.org/lucasvazq/cushead.py)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ce412113e4144c9f9739a99a0d0b77f5)](https://app.codacy.com/app/lucasvazq/cushead.py?utm_source=github.com&utm_medium=referral&utm_content=lucasvazq/cushead.py&utm_campaign=Badge_Grade_Dashboard)
[![codecov](https://codecov.io/gh/lucasvazq/cushead.py/branch/master/graph/badge.svg)](https://codecov.io/gh/lucasvazq/cushead.py)
[![PyPI version](https://badge.fury.io/py/cushead.py.svg)](https://badge.fury.io/py/cushead.py)

<p align="center">
  <img src="./logo.png">
</p>

# cushead.py

**A CLI that help you to improve the SEO and UX of your websites.**

**Works with:** _meta-tags, favicons, manifest, robots, browserconfig, sitemap, opensearch_

**Python Versions:** _>=3.5, <4.0_

**Package Version**: _3.0.0_

**Status:** _Production/Stable_

## Description

This script edits an html file adding some meta-tags and other stuff for
improving the SEO and the UX of your website. Also, it generate a lot of useful
files that are vinculated to that tags or stuff. For example, icons for apple
devices and manifest.json file. The info and the files generated can be set
through a config file.

The script can generate a full default config file running:

`cushead.py -preset example-config.txt`

You can edit that file how you want, and then run the script with that settings
using:

`cushead.py -file example-config.txt`

## MENU

[Install](#install)

[Arguments](#arguments)

1) [-h](#-h)

2) [-preset](#-preset)

3) [-file](#-file)

[Testing](#testing)

[Considerations](#considerations)

[License](#license)

## Install

`python3 -m pip install cushead.py`

## Arguments

### -h

`python3 cushead.py -h`

```txt
usage: cushead.py -file FILEPATH

Options (one required):
  -preset FILENAME  Name for config file. Generate an example config file. That
                    file contains a variable named 'config' that can be
                    customized. It has some required values: 'html_file' (FILE
                    PATH), 'output' (FOLDER PATH) and 'static_url' (STRING).
                    Also, if 'icon_png' (IMAGE FILE PATH) is declared, this
                    key need to have a value related to a path of an existing
                    image.
  -file FILEPATH    Path to config file. Read a config file that contains
                    configurable values related to SEO and UX. After it, the
                    script edits an html file and generate complementary files
                    like icons, robots.txt, etc.

Examples:
1) Generate config file:
    cushead.py -preset custom.txt
2) Execute with using that config file:
    cushead.py -file custom.txt
```

### -preset

This command generate a full config file in python syntax.
Example:

`cushead.py -preset config.txt`

_(config.txt)_
```python
"""
Python syntax
cushead.py config file
Git: https://github.com/lucasvazq/cushead.py
Documentation: https://github.com/lucasvazq/cushead.py/blob/master/README.md

CONFIG VARIABLES:

  html_file (FILE PATH):
    Required, can't be void, need to exist and referrer to a file

  output (FOLDER PATH):
    Required, need to exist and referrer to a folder

  static_url (STRING):
    Required

  icon_png (FILE PATH):
    If declared, need to exist and referrer to an image file
    Recomended 310x310 png image
"""

# Don't delete or change the name of this variable
config = {

  # MAIN CONFIG
  'html_file':        './index.html',
  'output':           './output/', # e.g. for manifest.json
  'static_url':       '/static/',

  # GENERAL CONFIG
  'content-type':     'text/html; charset=utf-8',
  'X-UA-Compatible':  'ie=edge',
  'viewport':         {'width': 'device-width', 'initial-scale': '1'},
  'locale':           'en_US',
  'type':             'website', # http://ogp.me/#types
  'color':            '#FFFFFF',
  'url':              'microsoft.com', # Without "www." and protocol (e.g. "http://")
  'protocol':         'https://',
  'robots':           'index, follow',
  'browserconfig':    'browserconfig.xml',
  'manifest':         'manifest.json',
  'opensearch':       'opensearch.xml',
  'sitemap':          'sitemap.xml',

  # BASIC CONFIG
  'title':            'Microsoft',
  'description':      'Technology Solutions',
  'subject':          'Home Page',
  'keywords':         'Microsoft, Windows',

  # IMAGES
  'preview':          'preview.png', # Big image preview
  'preview_type':     'image/png', # image/jpeg, image/gif or image/png
  'icon':             'favicon.ico', # *.ico
  'icon_png':         './favicon.png', # FILEPATH PNG IMAGE 310x310
  'mask-icon':        'maskicon.svg', # svg file type

  # SOCIAL MEDIA
  'fb:app_id':        '12345', # Facebook App ID
  'tw:site':          '@Microsoft', # Twitter account
  'tw:creator:id':    '123456', # Page editor ID

  # PWA
  'dir':              'ltr',
  'start_url':        '/',
  'orientation':      'landscape',
  'scope':            '/',
  'display':          'browser',
  'platform':        'web',
  'applications':     [
    {
      'platform': 'play',
      'url':      'https://play.google.com/store/apps/details?id=com.example.app',
      'id':       'com.example.app'
    },
    {
      'platform': 'itunes',
      'url':      'https://itunes.apple.com/app/example-app/id123456',
    }
  ],

  # AUTHOR
  'author':           'Lucas Vazquez'

}
```

#### html_file

Requires for a *.html file path.
That file needs to contain a literally `<html>` element and a $head$ variable.
The `<html>`element is used to add the lang attribute.
The $head$ variable is used to be replaced with custom elements like meta-tags.
Example struct:

_(index.html)_
```html
<html>
  <head>
    $head$
  </head>
</html>
```

#### output

The folder where all generated files are going to be saved.
It must exist.

#### static_url

The URL path of statics files.

#### icon_png

A PNG image file used to generate the icons. 310x310 size recommended.

### -file

This argument uses a config file to run the script.
Using the default config file generated with -preset, we run the script with
-file:

`cushead.py -file config.txt`

Output:
```txt
HTML:
<html lang="en_US">

HEAD:
<!-- Custom head elements -->
<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
<meta http-equiv='X-UA-Compatible' content='ie=edge' />
<meta name='viewport' content='width=device-width, initial-scale=1' />
<meta http-equiv='Content-Language' content='en_US' />
<meta name='theme-color' content='#FFFFFF' />
<meta name='msapplication-TileColor' content='#FFFFFF' />
<meta name='robots' content='index, follow' />
<title>Microsoft</title>
<meta name='application-name' content='Microsoft'>
<meta name='description' content='Technology Solutions' />
<meta name='subject' content='Home Page' />
<meta name='keywords' content='Microsoft, Windows' />
<link rel='icon' type="image/png" sizes='16x16' href='/static/favicon-16x16.png' />
<link rel='icon' type="image/png" sizes='24x24' href='/static/favicon-24x24.png' />
<link rel='icon' type="image/png" sizes='32x32' href='/static/favicon-32x32.png' />
<link rel='icon' type="image/png" sizes='48x48' href='/static/favicon-48x48.png' />
<link rel='icon' type="image/png" sizes='57x57' href='/static/favicon-57x57.png' />
<link rel='icon' type="image/png" sizes='60x60' href='/static/favicon-60x60.png' />
<link rel='icon' type="image/png" sizes='64x64' href='/static/favicon-64x64.png' />
<link rel='icon' type="image/png" sizes='70x70' href='/static/favicon-70x70.png' />
<link rel='icon' type="image/png" sizes='72x72' href='/static/favicon-72x72.png' />
<link rel='icon' type="image/png" sizes='76x76' href='/static/favicon-76x76.png' />
<link rel='icon' type="image/png" sizes='96x96' href='/static/favicon-96x96.png' />
<link rel='icon' type="image/png" sizes='114x114' href='/static/favicon-114x114.png' />
<link rel='icon' type="image/png" sizes='120x120' href='/static/favicon-120x120.png' />
<link rel='icon' type="image/png" sizes='128x128' href='/static/favicon-128x128.png' />
<link rel='icon' type="image/png" sizes='144x144' href='/static/favicon-144x144.png' />
<link rel='icon' type="image/png" sizes='150x150' href='/static/favicon-150x150.png' />
<link rel='icon' type="image/png" sizes='152x152' href='/static/favicon-152x152.png' />
<link rel='icon' type="image/png" sizes='167x167' href='/static/favicon-167x167.png' />
<link rel='icon' type="image/png" sizes='180x180' href='/static/favicon-180x180.png' />
<link rel='icon' type="image/png" sizes='192x192' href='/static/favicon-192x192.png' />
<link rel='icon' type="image/png" sizes='195x195' href='/static/favicon-195x195.png' />
<link rel='icon' type="image/png" sizes='196x196' href='/static/favicon-196x196.png' />
<link rel='icon' type="image/png" sizes='228x228' href='/static/favicon-228x228.png' />
<link rel='icon' type="image/png" sizes='310x310' href='/static/favicon-310x310.png' />
<meta name='msapplication-TileImage' content='/static/ms-icon-144x144.png' />
<link rel='apple-touch-icon' href='/static/apple-touch-icon-57x57.png' />
<link rel='apple-touch-icon' sizes='57x57' href='/static/apple-touch-icon-57x57.png' />
<link rel='apple-touch-icon' sizes='60x60' href='/static/apple-touch-icon-60x60.png' />
<link rel='apple-touch-icon' sizes='72x72' href='/static/apple-touch-icon-72x72.png' />
<link rel='apple-touch-icon' sizes='76x76' href='/static/apple-touch-icon-76x76.png' />
<link rel='apple-touch-icon' sizes='114x114' href='/static/apple-touch-icon-114x114.png' />
<link rel='apple-touch-icon' sizes='120x120' href='/static/apple-touch-icon-120x120.png' />
<link rel='apple-touch-icon' sizes='144x144' href='/static/apple-touch-icon-144x144.png' />
<link rel='apple-touch-icon' sizes='152x152' href='/static/apple-touch-icon-152x152.png' />
<link rel='apple-touch-icon' sizes='180x180' href='/static/apple-touch-icon-180x180.png' />
<link rel='fluid-icon' href='/static/fluidicon-512x512.png' title='Microsoft' />
<link rel='shortcut icon' href='/static/favicon.ico' type='image/x-icon' />
<link rel='mask-icon' href='maskicon.svg' color='#FFFFFF' />
<meta name='msapplication-config' content='/static/browserconfig.xml' />
<link rel='manifest' href='/static/manifest.json' />
<link rel='search' type='application/opensearchdescription+xml' title='Microsoft' href='/static/opensearch.xml' />
<meta porperty='fb:app_id' content='12345' />
<meta property='og:locale' content='en_US' />
<meta property='og:type' content='website' />
<meta property='og:url' content='https://microsoft.com' />
<meta property='og:site_name' content='Microsoft' />
<meta property='og:title' content='Microsoft' />
<meta property='og:description' content='Technology Solutions' />
<meta property='og:image' content='/static/preview.png' />
<meta property='og:image:secure_url' content='/static/preview.png' />
<meta name='twitter:image' content='/static/preview.png' />
<meta property='og:image:type' content='image/png' />
<meta property='og:image:alt' content='Microsoft - Technology Solutions' />
<meta name='twitter:image:alt' content='Microsoft - Technology Solutions' />
<meta name='twitter:card' content='summary' />
<meta name='twitter:site' content='@Microsoft' />
<meta name='twitter:title' content='Microsoft' />
<meta name='twitter:description' content='Technology Solutions' />
<meta property='twitter:creator:id' content='123456' />
<meta name='author' content='Lucas Vazquez' />

NEW FILES:
./output/favicon-16x16.png
./output/favicon-24x24.png
./output/favicon-32x32.png
./output/favicon-48x48.png
./output/favicon-57x57.png
./output/favicon-60x60.png
./output/favicon-64x64.png
./output/favicon-70x70.png
./output/favicon-72x72.png
./output/favicon-76x76.png
./output/favicon-96x96.png
./output/favicon-114x114.png
./output/favicon-120x120.png
./output/favicon-128x128.png
./output/favicon-144x144.png
./output/favicon-150x150.png
./output/favicon-152x152.png
./output/favicon-167x167.png
./output/favicon-180x180.png
./output/favicon-192x192.png
./output/favicon-195x195.png
./output/favicon-196x196.png
./output/favicon-228x228.png
./output/favicon-310x310.png
./output/ms-icon-144x144.png
./output/apple-touch-icon-57x57.png
./output/apple-touch-icon-57x57.png
./output/apple-touch-icon-60x60.png
./output/apple-touch-icon-72x72.png
./output/apple-touch-icon-76x76.png
./output/apple-touch-icon-114x114.png
./output/apple-touch-icon-120x120.png
./output/apple-touch-icon-144x144.png
./output/apple-touch-icon-152x152.png
./output/apple-touch-icon-180x180.png
./output/fluidicon-512x512.png
./output/ms-icon-30x30.png
./output/ms-icon-44x44.png
./output/ms-icon-70x70.png
./output/ms-icon-150x150.png
./output/ms-icon-310x310.png
./output/ms-icon-310x150.png
./output/android-icon-36x36.png
./output/android-icon-48x48.png
./output/android-icon-72x72.png
./output/android-icon-96x96.png
./output/android-icon-144x144.png
./output/android-icon-192x192.png
./output/opensearch-16x16.png
./output/browserconfig.xml
./output/manifest.json
./output/opensearch.xml
./output/robots.txt
./output/sitemap.xml

HTML FILE: ./index.html
(full path): /home/user/Documents/Projects/Websites/Example/./index.html
OUTPUT FILES: ./output/
(full path): /home/user/Documents/Projects/Websites/Example/./output/
```

#### Edited html file

Supposing we provide the html file declared previously (index.html), the result
will be:

_(index.html)_
```html
<html lang="en_US">
	<head>
		<!-- Custom head elements -->
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta http-equiv="X-UA-Compatible" content="ie=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<meta http-equiv="Content-Language" content="en_US" />
		<meta name="theme-color" content="#FFFFFF" />
		<meta name="msapplication-TileColor" content="#FFFFFF" />
		<meta name="robots" content="index, follow" />
		<title>Microsoft</title>
		<meta name="application-name" content="Microsoft">
		<meta name="description" content="Technology Solutions" />
		<meta name="subject" content="Home Page" />
		<meta name="keywords" content="Microsoft, Windows" />
		<link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png" />
		<link rel="icon" type="image/png" sizes="24x24" href="/static/favicon-24x24.png" />
		<link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png" />
		<link rel="icon" type="image/png" sizes="48x48" href="/static/favicon-48x48.png" />
		<link rel="icon" type="image/png" sizes="57x57" href="/static/favicon-57x57.png" />
		<link rel="icon" type="image/png" sizes="60x60" href="/static/favicon-60x60.png" />
		<link rel="icon" type="image/png" sizes="64x64" href="/static/favicon-64x64.png" />
		<link rel="icon" type="image/png" sizes="70x70" href="/static/favicon-70x70.png" />
		<link rel="icon" type="image/png" sizes="72x72" href="/static/favicon-72x72.png" />
		<link rel="icon" type="image/png" sizes="76x76" href="/static/favicon-76x76.png" />
		<link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png" />
		<link rel="icon" type="image/png" sizes="114x114" href="/static/favicon-114x114.png" />
		<link rel="icon" type="image/png" sizes="120x120" href="/static/favicon-120x120.png" />
		<link rel="icon" type="image/png" sizes="128x128" href="/static/favicon-128x128.png" />
		<link rel="icon" type="image/png" sizes="144x144" href="/static/favicon-144x144.png" />
		<link rel="icon" type="image/png" sizes="150x150" href="/static/favicon-150x150.png" />
		<link rel="icon" type="image/png" sizes="152x152" href="/static/favicon-152x152.png" />
		<link rel="icon" type="image/png" sizes="167x167" href="/static/favicon-167x167.png" />
		<link rel="icon" type="image/png" sizes="180x180" href="/static/favicon-180x180.png" />
		<link rel="icon" type="image/png" sizes="192x192" href="/static/favicon-192x192.png" />
		<link rel="icon" type="image/png" sizes="195x195" href="/static/favicon-195x195.png" />
		<link rel="icon" type="image/png" sizes="196x196" href="/static/favicon-196x196.png" />
		<link rel="icon" type="image/png" sizes="228x228" href="/static/favicon-228x228.png" />
		<link rel="icon" type="image/png" sizes="310x310" href="/static/favicon-310x310.png" />
		<meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png" />
		<link rel="apple-touch-icon" href="/static/apple-touch-icon-57x57.png" />
		<link rel="apple-touch-icon" sizes="57x57" href="/static/apple-touch-icon-57x57.png" />
		<link rel="apple-touch-icon" sizes="60x60" href="/static/apple-touch-icon-60x60.png" />
		<link rel="apple-touch-icon" sizes="72x72" href="/static/apple-touch-icon-72x72.png" />
		<link rel="apple-touch-icon" sizes="76x76" href="/static/apple-touch-icon-76x76.png" />
		<link rel="apple-touch-icon" sizes="114x114" href="/static/apple-touch-icon-114x114.png" />
		<link rel="apple-touch-icon" sizes="120x120" href="/static/apple-touch-icon-120x120.png" />
		<link rel="apple-touch-icon" sizes="144x144" href="/static/apple-touch-icon-144x144.png" />
		<link rel="apple-touch-icon" sizes="152x152" href="/static/apple-touch-icon-152x152.png" />
		<link rel="apple-touch-icon" sizes="180x180" href="/static/apple-touch-icon-180x180.png" />
		<link rel="fluid-icon" href="/static/fluidicon-512x512.png" title="Microsoft" />
		<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon" />
		<link rel="mask-icon" href="maskicon.svg" color="#FFFFFF" />
		<meta name="msapplication-config" content="/static/browserconfig.xml" />
		<link rel="manifest" href="/static/manifest.json" />
		<link rel="search" type="application/opensearchdescription+xml" title="Microsoft" href="/static/opensearch.xml" />
		<meta porperty="fb:app_id" content="12345" />
		<meta property="og:locale" content="en_US" />
		<meta property="og:type" content="website" />
		<meta property="og:url" content="https://microsoft.com" />
		<meta property="og:site_name" content="Microsoft" />
		<meta property="og:title" content="Microsoft" />
		<meta property="og:description" content="Technology Solutions" />
		<meta property="og:image" content="/static/preview.png" />
		<meta property="og:image:secure_url" content="/static/preview.png" />
		<meta name="twitter:image" content="/static/preview.png" />
		<meta property="og:image:type" content="image/png" />
		<meta property="og:image:alt" content="Microsoft - Technology Solutions" />
		<meta name="twitter:image:alt" content="Microsoft - Technology Solutions" />
		<meta name="twitter:card" content="summary" />
		<meta name="twitter:site" content="@Microsoft" />
		<meta name="twitter:title" content="Microsoft" />
		<meta name="twitter:description" content="Technology Solutions" />
		<meta property="twitter:creator:id" content="123456" />
		<meta name="author" content="Lucas Vazquez" />
	</head>
</html>
```

#### New files

48 new icons with different sizes, coming from 'icon_png' config value.
New files: browserconfig.xml, manifest.json, opensearch.xml, robots.txt and
sitemap.xml

_(browserconfig.xml)_ _BEAUTY VERSION_
```xml
<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square30x30logo src="/static/ms-icon-30x30.png" />
      <square44x44logo src="/static/ms-icon-44x44.png" />
      <square70x70logo src="/static/ms-icon-70x70.png" />
      <square150x150logo src="/static/ms-icon-150x150.png" />
      <square310x310logo src="/static/ms-icon-310x310.png" />
      <wide310x150logo src="/static/ms-icon-310x150.png" />
      <TileColor>#FFFFFF</TileColor>
    </tile>
  </msapplication>
</browserconfig>
```

_(manifest.json)_ _BEAUTY VERSION_
```json
{
  "name": "Microsoft",
  "short_name": "Microsoft",
  "description": "Technology Solutions",
  "dir": "ltr",
  "start_url": "/",
  "orientation": "landscape",
  "background_color": "#FFFFFF",
  "theme_color": "#FFFFFF",
  "locale": "en_US",
  "scope": "/",
  "display": "browser",
  "platform": "web",
  "related_applications": [
    {
      "platform": "play",
      "url": "https://play.google.com/store/apps/details?id=com.example.app",
      "id": "com.example.app"
    },
    {
      "platform": "itunes",
      "url": "https://itunes.apple.com/app/example-app/id123456"
    }
  ],
  "icons": [
    {
      "src": "/static/android-icon-36x36",
      "sizes": "36x36",
      "type": "image/png",
      "density": "0.75"
    },
    {
      "src": "/static/android-icon-48x48",
      "sizes": "48x48",
      "type": "image/png",
      "density": "1.0"
    },
    {
      "src": "/static/android-icon-72x72",
      "sizes": "72x72",
      "type": "image/png",
      "density": "1.5"
    },
    {
      "src": "/static/android-icon-96x96",
      "sizes": "96x96",
      "type": "image/png",
      "density": "2.0"
    },
    {
      "src": "/static/android-icon-144x144",
      "sizes": "144x144",
      "type": "image/png",
      "density": "3.0"
    },
    {
      "src": "/static/android-icon-192x192",
      "sizes": "192x192",
      "type": "image/png",
      "density": "4.0"
    }
  ]
}
```

_(opensearch.xml)_ _BEAUTY VERSION_
```xml
<?xml version="1.0" encoding="utf-8"?>
<OpenSearchDescription xmlns:moz="http://www.mozilla.org/2006/browser/search/" xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>Microsoft</ShortName>
  <Description>Search Microsoft</Description>
  <InputEncoding>UTF-8</InputEncoding>
  <Url method="get" type="text/html" template="http://www.google.com/search?q={searchTerms}+site%3Amicrosoft.com" />
  <Image height="16" width="16" type="image/png">/static/opensearch-16x16.png</Image>
</OpenSearchDescription>
```

_(robots.txt)_
```txt
User-agent: *
Allow: /

Sitemap: https://microsoft.com/sitemap.xml
```

_(sitemap.xml)_ _BEAUTY VERSION_
```xml
<?xml version="1.0" encoding="uft-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  <url>
    <loc>https://microsoft.com/</loc>
  </url>
</urlset>
```

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

Here is a list of concepts that comprise good practices to improve SEO and UX:

1) Structured data: RDFa, JSON-D, Microdata, GoodRelations, vCard, hCard
2) rel profile attribute for referring to author or website owner
3) Maskable icons
4) Accelerated Mobiles Pages
5) Progressive Web Apps
6) Screenshots in manifest for PWA
7) Add PWA to App stores (like the Play Store of Google)
8) Javascript and css minified and purged with short variables names
9) Responsive Design
10) Mobile call and Whatsapp sms for mobiles websites
11) Google my Business integration
12) gzip and bzip2 compression
13) Server Side Rendering
14) HTTP caching in Client Side
15) Content Delivery Network

## License

**cushead.py** © 2019 Lucas Vazquez. Released under the [MIT](http://mit-license.org/) License.
