class Company:

    def __init__(self, name_: str, slug_: str, template_name_: str, social_media_: {}):
        self.name = name_
        self.slug = slug_
        self.template_name = template_name_
        self.social_media = social_media_

    def __str__(self):
        return "%s %s %s" % (self.name, self.slug, self.social_media)

    def __repr__(self):
        return "%s %s %s" % (self.name, self.slug, self.social_media)