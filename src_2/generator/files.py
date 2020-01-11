

class Index:
    config = {}

    def base():
        language = self.config["language"]
        return (
            f"<html lang='{language}'>\n"
            f"{self.head()}\n"
            f"{self.body()}\n"
            "</html>"
        ).replace("'", '"')

    def head():
        head = []

        # content-type
        head.append(f"<meta http-equiv='Content-Type' content='{self.config["content-type"]}'>")
        # X-UA-Compatible
        head.append(f"<meta http-equiv='X-UA-Compatible' "
                    f"content='{self.config["X-UA-Compatible"]}'>")
        # viewport
        head.append(f"<meta name='viewport' content='{self.config["viewport"]}'>")
        # locale
        head.append(f"<meta http-equiv='Content-Language' "
                    f"content='{self.config["language"]}'>")
        # robots
        head.append(f"<meta name='robots' content='{self.config["robots"]}'>")
        # apple
        head.extend([
            "<meta name='apple-mobile-web-app-capable' content='yes'>",
            ("<meta name='apple-mobile-web-app-status-bar-style' "
             "content='black-translucent'>"),
        ])
    
        # title
        head.extend([
            f"<title>{self.config["title"]}</title>",
            f"<meta name='application-name' content='{self.config["title"]}'>",
            f"<meta name='apple-mobile-web-app-title' "
            f"content='{self.config["title"]}'>",
        ])
        # description
        head.append(f"<meta name='description' content='{self.config["description"]}'>")
        # subject
        head.append(f"<meta name='subject' content='{self.config["subject"]}'>")
        # theme-color and msapplication-TileColor
        head.extend([
            f"<meta name='theme-color' content='{self.config["background_color"]}'>",
            f"<meta name='msapplication-TileColor' content='{self.config["background_color"]}'>",
        ])
        # author
        head.append(f"<meta name='author' content='{self.config["author"]}'>")

        # IMAGES
        # ==============

        title = self.config.get("title", "")
    
        # browserconfig.xml
        head.append(f"<meta name='msapplication-config' content='{self.config["static_url"]}/browserconfig.xml'>")
        # manifest.json
        head.append(f"<link rel='manifest' href='{self.config["static_url"]}/manifest.json'>")
        # opensearch.xml
        head.append(
            f"<link rel='search' type='application/opensearchdescription+xml' title='{self.config["title"]}' href='{self.config["static_url"]}/opensearch.xml'>"
        )

        # fb:app_id
        head.append(f"<meta porperty='fb:app_id' content='{self.config["facebook_app_id"]}'>")
        # og:locale
        head.append(f"<meta property='og:locale' content='{self.config["language"]}_{self.config["territory"]}'>")
        # og:type
        # Only allow website type for simplicity
        head.append("<meta property='og:type' content='website'>")
        # og:url, Likes and Shared are stored under this url
        string = self.config.get("protocol", "")
        string += self.config.get("clean_url", "")
        head.append(f"<meta property='og:url' content='{string}'>")
        # og:site_name
        head.append(f"<meta property='og:site_name' content='{self.config["title"]}'>")
        # og:title
        head.append(f"<meta property='og:title' content='{self.config["title"]}'>")
        # og:description
        head.append(f"<meta property='og:description' content='{self.config["description"]}'>")
        # og:image:type
        # Only allow png type for simplicity
        head.append("<meta property='og:image:type' content='image/png'>")
        # og:image:alt
        head.append(f"<meta property='og:image:alt' content='{self.config["title"]} - {self.config["description"]}'>")

        # twitter:card
        # Only allow summary type for simplicity
        head.append("<meta name='twitter:card' content='summary'>")
        # twitter:site
        head.append(f"<meta name='twitter:site' content='{self.config["twitter_user_@"]}'>")
        # twitter:title
        head.append(f"<meta name='twitter:title' content='{self.config["title"]}'>")
        # twitter:description
        head.append(f"<meta name='twitter:description' content='{self.config["description"]}'>")
        # tw:creator
        head.append(f"<meta property='twitter:creator:id' "
                    f"content='{self.config["twitter_user_id"]}'>")
        # tw:image:alt
        head.append(f"<meta name='twitter:image:alt' content='{self.config["title"]} - {self.config["description"]}'>")

        json_ld_dict = {
            "@context": "http://schema.org/",
            "@type": "Organization",
            "@id": f"{self.config["protocol"]}{self.config["clean_url"]}",
            "url": f"{self.config["protocol"]}{self.config["clean_url"]}",
            "slogan": self.config["description"],
            "description": self.config["description"],
            "logo": f"{self.config["protocol"]}{self.config["clean_url"]}/static/preview_500x500.png", # CHECK IT
            "image": f"{self.config["protocol"]}{self.config["clean_url"]}/static/preview_500x500.png", # CHECK IT
        }
        head.append(
            f"<script type='application/ld+json'>{json.dumps(json_ld_dict)}</script>"
        )

        # convert to string adding ident
        return "    <head>\n" + "".join(
            [f"        {tag}\n" for tag in head]
        ) + "    </head>"

    def body():
        return "    <body></body>"
