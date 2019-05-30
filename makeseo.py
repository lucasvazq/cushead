'''
TODO
 + Google website proprietary
 + x-ua-compatible
 + manifiest
'''


from os import fdopen, remove
from shutil import move
from tempfile import mkstemp


'''
Get a file and add lang tag to <html> and replace $head$ with custom SEO elements

Repository:
    github https://github.com/mrsantos321/MakeSEO


Usage:
    Edit the dictionary and add in 'path' key the main file where u want to add the custom elements

Example:

    dictionary = {

        # File path
        'path':             './index.html',

        # Basic
        'title':            'Microsoft',
        'icon':             '/favicon.png',
        'preview':          '/preview.png', # Big image preview
        'description':      'Technology Solutions',
        'subject':          'Home Page',
        'keywords':         'Microsoft, Windows',

        # Facebook
        'fb:pages':         {'12345', '67890'}, # (Str) Facebook Pages ID separated by commas
        'fb:app_id':        '12345', # (Str) Facebook App ID

        # Twitter
        'twitter:page':     '@Microsoft', # Commerce Twitter account
        'twitter:creator':  '@BillGates', # This page editor

        # Phone apps.
        'googleplay':       '12345', # Google Play app id
        'ipad':             '12345', # iPad app id
        'iphone':           '12345', # iPhone app id

        # Other
        'domain':           'www.microsoft.com',
        'type':             'website', # http://ogp.me/#types
        'twitter:card':     'summary', # https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/summary.html
        'locale':           'en_US',

        # Web author
        'author':           'Lucas Vazquez'
        
    }
'''

dictionary = {

    # File path
    'path':             './index.html',

    # Basic
    'title':            'Microsoft',
    'icon':             '/favicon.png',
    'preview':          '/preview.png', # Big image preview
    'description':      'Technology Solutions',
    'subject':          'Home Page',
    'keywords':         'Microsoft, Windows',

    # Facebook
    'fb:pages':         {'12345', '67890'}, # (Str) Facebook Pages ID separated by commas
    'fb:app_id':        '12345', # (Str) Facebook App ID

    # Twitter
    'twitter:page':     '@Microsoft', # Commerce Twitter account
    'twitter:creator':  '@BillGates', # This page editor

    # Phone apps.
    'googleplay':       '12345', # Google Play app id
    'ipad':             '12345', # iPad app id
    'iphone':           '12345', # iPhone app id

    # Other
    'domain':           'www.microsoft.com',
    'type':             'website', # http://ogp.me/#types
    'twitter:card':     'summary', # https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/summary.html
    'locale':           'en_US',

    # Web author
    'author':           'Lucas Vazquez'
    
}

def seo(dictionary):

    if not len(dictionary['path']):
        print('Miss \'path\' key on dictionary')
        exit()

    temp = []

    ''' Basic SEO '''
    # title
    if len(dictionary['title']):
        temp.append('<title>' + dictionary['title'] + '</title>')
    # icon
    if len(dictionary['icon']):
        temp.append('<link rel="shortcut icon" href="' + dictionary['icon'] + '" />')
    # description
    if len(dictionary['description']):
        temp.append('<meta name="description" content="' + dictionary['description'] + '" />')
    # subject
    if len(dictionary['subject']):
        temp.append('<meta name="subject" content="' + dictionary['subject'] + '" />')
    # keywords
    if len(dictionary['keywords']):
        temp.append('<meta name="keywords" content="' + dictionary['keywords'] + '" />')
    
    ''' Facebook '''
    # pages id
    if len(dictionary['fb:pages']):
        pages = ''
        for x in dictionary['fb:pages']:
            pages += x + ', '
        pages[0:-2]
        temp.append('<meta property="fb:pages" content="' + pages + '" />')
    # app id
    if len(dictionary['fb:app_id']):
        temp.append('<meta porperty="fb:app_id" content="' + dictionary['fb:app_id'] + '" />')

    ''' Open Graph '''
    # site name
    if len(dictionary['title']):
        temp.append('<meta property="og:site_name" content="' + dictionary['title'] + '" />')
    # title
    if len(dictionary['title']):
        temp.append('<meta property="og:title" content="' + dictionary['title'] + '" />')
    # preview (http)
    if len(dictionary['preview']):
        temp.append('<meta property="og:image" content="' + dictionary['preview'] + '" />')
    elif len(dictionary['icon']):
        temp.append('<meta property="og:image" content="' + dictionary['icon'] + '" />')
    # preview (https)
    if len(dictionary['preview']):
        temp.append('<meta property="og:image:secure_url" content="' + dictionary['preview'] + '" />')
    elif len(dictionary['icon']):
        temp.append('<meta property="og:image:secure_url" content="' + dictionary['icon'] + '" />')
    # description
    if len(dictionary['description']):
        temp.append('<meta property="og:description" content="' + dictionary['description'] + '" />')

    ''' Twitter '''
    # title
    if len(dictionary['title']):
        temp.append('<meta name="twitter:title" content="' + dictionary['title'] + '" />')
    # preview
    if len(dictionary['preview']):
        temp.append('<meta name="twitter:image" content="' + dictionary['preview'] + '" />')
    elif len(dictionary['icon']):
        temp.append('<meta name="twitter:image" content="' + dictionary['icon'] + '" />')
    # description
    if len(dictionary['description']):
        temp.append('<meta name="twitter:description" content="' + dictionary['description'] + '" />')
    # twitter commerce page
    if len(dictionary['twitter:page']):
        temp.append('<meta name="twitter:site" content="' + dictionary['twitter:page'] + '" />')
    # twitter commerce admin page
    if len(dictionary['twitter:creator']):
        temp.append('<meta property="twitter:creator" content="' + dictionary['twitter:creator'] + '" />')

    ''' Phone apps '''
    # google play
    if len(dictionary['googleplay']):
        temp.append('<meta property="twitter:app:id:googleplay" content="' + dictionary['googleplay'] + '" />')
    # ipad
    if len(dictionary['ipad']):
        temp.append('<meta property="twitter:app:id:ipad" content="' + dictionary['ipad'] + '" />')
    # iphone
    if len(dictionary['iphone']):
        temp.append('<meta property="twitter:app:id:iphone" content="' + dictionary['iphone'] + '" />')

    ''' Other '''
    # domain
    if len(dictionary['domain']):
        temp.append('<meta name="twitter:domain" content="' + dictionary['domain'] + '">')
    # type
    if len(dictionary['type']):
        temp.append('<meta property="og:type" content="' + dictionary['type'] + '" />')
    # card
    if len(dictionary['twitter:card']):
        temp.append('<meta name="twitter:card" content="' + dictionary['twitter:card'] + '">')
    # locale and language
    if len(dictionary['locale']):
        temp.append('<meta property="og:locale" content="' + dictionary['locale'] + '" />')
        temp.append('<meta http-equiv="Content-Language" content="' + dictionary['locale'] + '" />')

    ''' Web author '''
    # name
    if len(dictionary['author']):
        temp.append('<meta name="author" content="' + dictionary['author'] + '" />')

    ''' Add lang tag to html and replace $head$ '''

    # Read contents from file as a single string
    file_handle = open(dictionary['path'], 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Generate idented dom
    space = file_string.split('$head$')
    if not len(space) > 1:
        print('Miss $head$')
        exit()
    space = space[0].split('\n')
    space = space[len(space) - 1]
    print(space)
    concat = '\n' + space + '<!-- Autogenerated SEO elements -->\n'
    for x in temp:
        concat += space + x + '\n'
    
    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = file_string.replace('$head$', concat)
    if len(dictionary['locale']):
        file_string = file_string.replace('<html>', '<html lang="' + dictionary['locale'] + '">')

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(dictionary['path'], 'w')
    file_handle.write(file_string)
    file_handle.close()

    print(concat)
    print('PATH: ' + dictionary['path'])
    print('Done')

seo(dictionary)
