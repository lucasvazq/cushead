# MakeSEO.py

This simple script allows you to create custom SEO elements for your website.
It adds the lang tag to the html element and search and replace '$head$' string with the personalized elements.

### Usage

Before all, localize a file where u want to add the SEO elements and add '$head$' string where u want to put them.
ie:
´´´
<html>
  <head>
    $head$
    ...
    fonts, javascript, etc
  </head>
  ...
</html>
After it, open the script and edit the inside dictionary.
In 'path' key, u should put the main file where to want to add the elements.
