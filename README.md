# cushead.py
###### _Python 3_

This simple script improves your SEO and the UX. It adds lang attribute to the <html> element and search and replace '$head$' string with personalized head elements.

### Install:

`pip3 install cushead`

### Usage:

#### Fast view of the argument list

`cushead.py -h`

```
help:
  -presset FILENAME    Generate example file with pressets.

required arguments:
  -file FILEPATH       Path to file that want to edit.

optional arguments:
  --exclude-comment    Exclude 'Custom head elements' comment.
  --exclude-html       Exclude html lang attribute.
  --exclude-special    Exclude special head elements.
  --exclude-basic      Exclude basic SEO elements.
  --exclude-opengraph  Exclude opengraph.
  --exclude-facebook   Exclude facebook.
  --exclude-twitter    Exclude twitter.
  --exclude-author     Exclude author.
```

#### 1 - Find the main file

This is the file that wants to edit. It needs to have the <html> element for add the lang attribute, and a '$head$' string that be replaced for the custom elements. Example:

_(my_index.html)_
```
<html> 
    <head>
        $head$
        ...
    </head>
</html>
```

If there isn't the <html> element, cant add the lang attribute. Same way, if there isn't the '$head$' string, cant add the custom head elements.

#### 2 - Define personalized values

Create a file with this inside:

_(cushead.txt)_
```
values = {

    # FILE PATH
    'path':             './my_index.html',

    # BASIC CONFIG
    'content-type':     'text/html; charset=utf-8',
    'X-UA-Compatible':  'ie=edge',
    'robots':           'index, follow',
    'manifest':         '/manifest.json',
    'msapp-config':     '/browserconfig.xml',
    'viewport':         {'width': 'device-width', 'initial-scale': '1'},
    'locale':           'en_US',

    # BASIC SEO
    'title':            'Microsoft',
    'description':      'Technology Solutions',
    'icon':             '/static/favicon.png',
    'subject':          'Home Page',
    'keywords':         'Microsoft, Windows',

    # SOCIAL MEDIA

    # General
    'preview':          '/static/preview.png', # Big image preview

    # Opengraph
    # og:title, og:description, og:image, og:image:secure_url and og:locale obtained
    # from BASIC SEO and BASIC CONFIG sections.
    'og:url':            'www.microsoft.com',
    'og:type':          'website', # http://ogp.me/#types
    'og:image:type':    'image/png', # image/jpeg, image/gif or image/png

    # Facebook
    'fb:app_id':        '12345', # (Str) Facebook App ID

    # Twitter
    # Only support twitter:card = summary
    # twitter:title, twitter:description, twitter:image and twitter:image:alt
    # obtained from BASIC SEO and General - SOCIAL MEDIA sections.
    'tw:site':          '@Microsoft', # Commerce Twitter account
    'tw:creator:id':    '123456', # Page editor ID
    
    # AUTHOR
    'author':           'Lucas Vazquez'
    
}
```

Look, there is a dictionary called values, they are used to pass values to the script. Please, don't change the dictionary 'values' name. Feel free to add comments like python inside the dict. In values there is a key called 'path', this referred to the path where is the file that you want to edit. If some keys are omitted, the elements referred to them are omitted too.
File like this can be generated with doing `python3 cushead.py -presset cushead.txt`

#### 3 - Execute the script

`cushead.py -file cushead.txt --exclude-twitter`

#### 4 - Results

_(my_index.html)_
```
<html lang="en_US">
    <head>
        <!-- Custom head elements -->
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
        <meta name="robots" content="index, follow" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta http-equiv="Content-Language" content="en_US" />
        <title>Microsoft</title>
        <meta name="description" content="Technology Solutions" />
        <link rel="shortcut icon" href="/static/favicon.png" />
        <meta name="subject" content="Home Page" />
        <meta name="keywords" content="Microsoft, Windows" />
        <meta property="og:locale" content="en_US" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="www.microsoft.com" />
        <meta property="og:site_name" content="Microsoft" />
        <meta property="og:title" content="Microsoft" />
        <meta property="og:description" content="Technology Solutions" />
        <meta property="og:image" content="/static/preview.png" />
        <meta property="og:image:secure_url" content="/static/preview.png" />
        <meta property="og:image:type" content="image/png" />
        <meta name="og:image:alt" content="Microsoft - Technology Solutions" />
        <meta porperty="fb:app_id" content="12345" />
        <meta name="author" content="Lucas Vazquez" />
    </head>
</html>
```
