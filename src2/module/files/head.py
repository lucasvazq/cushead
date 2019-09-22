from .images import Images

class Head(Images):
    config = {}

    def general_config(self):
        """General config section"""
        # content-type
        head = []
        if 'content-type' in self.config:
            head.append("<meta http-equiv='Content-Type' "
                        f"content='{self.config['content-type']}' />")
        # X-UA-Compatible
        if 'X-UA-Compatible' in self.config:
            head.append("<meta http-equiv='X-UA-Compatible' "
                        f"content='{self.config['X-UA-Compatible']}' />")
        # viewport
        if 'viewport' in self.config:
            head.append("<meta name='viewport' "
                        f"content='{self.config['viewport']}' />")
        # locale
        if 'language' in self.config:
            head.append("<meta http-equiv='Content-Language' "
                        f"content='{self.config['language']}' />")
        # robots
        if 'robots' in self.config:
            head.append("<meta name='robots' "
                        f"content='{self.config['robots']}' />")
        # apple
        # Multiline strings inside a list get together into a parentheses
        head.extend([
            "<meta name='apple-mobile-web-app-capable' content='yes'>",
            ("<meta name='apple-mobile-web-app-status-bar-style' "
             "content='black-translucent'>"),
        ])
        return head

    def basic_config(self):
        """Basic config section"""
        head = []
        # title
        if 'title' in self.config:
            title = self.config['title']
            title_components = [
                f"<title>{title}</title>",
                f"<meta name='application-name' content='{title}' />",
                "<meta name='apple-mobile-web-app-title' "
                f"content='{title}' />",
            ]
            head.extend(title_components)
        # description
        if 'description' in self.config:
            head.append("<meta name='description' "
                        f"content='{self.config['description']}' />")
        # subject
        if 'subject' in self.config:
            head.append("<meta name='subject' "
                        f"content='{self.config['subject']}' />")
        # keywords
        if 'keywords' in self.config:
            head.append("<meta name='keywords' "
                        f"content='{self.config['keywords']}' />")
        # theme-color and msapplication-TileColor
        if 'background_color' in self.config:
            color = self.config['background_color']
            color_components = [
                f"<meta name='theme-color' content='{color}' />",
                f"<meta name='msapplication-TileColor' content='{color}' />",
            ]
            head.extend(color_components)
        # author
        if 'author' in self.config:
            head.append("<meta name='author' "
                        f"content='{self.config['author']}' />")
        return head

    def social_media(self):
        """Social media section"""
        head = []

        # OPENGRAPH AND FACEBOOK

        # fb:app_id
        if 'facebook_app_id' in self.config:
            head.append("<meta porperty='fb:app_id' "
                        f"content='{self.config['facebook_app_id']}' />")
        # og:locale
        if 'language' in self.config:
            territory = (
                "_{}".format(self.config['territory'])
                if 'territory' in self.config else ''
            )
            head.append("<meta property='og:locale' "
                        f"content='{self.config['language']}{territory}' />")
        # og:type
        # Only allow website type for simplicity
        head.append("<meta property='og:type' content='website' />")
        # og:url, Likes and Shared are stored under this url
        if 'clean_url' in self.config:
            head.append(f"<meta property='og:url' "
                        f"content='{self.config.get('protocol', '')}"
                        f"{self.config['clean_url']}' />")
        # og:site_name
        if 'title' in self.config:
            head.append("<meta property='og:site_name' "
                        f"content='{self.config['title']}' />")
        # og:title
        if 'title' in self.config:
            head.append("<meta property='og:title' "
                        f"content='{self.config['title']}' />")
        # og:description
        if 'description' in self.config:
            head.append("<meta property='og:description' "
                        f"content='{self.config['description']}' />")
        # og:image:type
        # Only allow png type for simplicity
        head.append("<meta property='og:image:type' content='image/png' />")
        # og:image:alt and twitter:image:alt
        if 'title' in self.config or 'description' in self.config:
            title = self.config.get('title', '')
            description = self.config.get('description', '')
            connector = (' - ' if ('title' in self.config and
                                   'description' in self.config) else '')
            text = title + connector + description
            head.extend([
                f"<meta property='og:image:alt' content='{text}' />",
                f"<meta name='twitter:image:alt' content='{text}' />",
            ])

        # TWITTER
        # twitter:image mixed with op:image and op:image:secure in OPENGRAH
        # section
        # twitter:image:alt mixed with op:image:alt in OPENGRAPH section

        # twitter:card
        # Only allow summary type for simplicity
        head.append("<meta name='twitter:card' content='summary' />")
        # twitter:site
        if 'twitter_user_@' in self.config:
            head.append("<meta name='twitter:site' "
                        f"content='{self.config['twitter_user_@']}' />")
        # twitter:title
        if 'title' in self.config:
            head.append("<meta name='twitter:title' "
                        f"content='{self.config['title']}' />")
        # twitter:description
        if 'description' in self.config:
            head.append("<meta name='twitter:description' "
                        f"content='{self.config['description']}' />")
        # tw:creator
        if 'twitter_user_id' in self.config:
            head.append("<meta property='twitter:creator:id' "
                        f"content='{self.config['twitter_user_id']}' />")

        return head
    
    def complementary_files(self):
        static_url = self.config.get('static_url', '')
        title = self.config.get('title', '')
        return [
            # browserconfig.xml
            ( "<meta name='msapplication-config' "
              f"content='{static_url}browserconfig.xml' />"),
            # manifest.json
            (f"<link rel='manifest' href='{static_url}"
             f"manifest.json' />"),
            # opensearch.xml
            ( "<link rel='search' "
             f"type='application/opensearchdescription+xml' "
             f"title='{title}' href='{static_url}"
              "opensearch.xml' />"),
        ]

    def full_head(self):
        head = [
            self.general_config(),
            self.basic_config(),
            self.favicon_ico(),
            self.favicon_png(),
            self.favicon_svg(),
            self.complementary_files(),
            self.social_media(),
        ]
        return head

