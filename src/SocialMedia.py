class SocialMedia:
    def __init__(self, name_, social_link_, social_icon_, company_slug_):
        self.name = name_
        self.link = social_link_
        self.icon_link = social_icon_
        self.company_slug = company_slug_

    def __str__(self):
        return "%s %s %s %s" % (self.name, self.link, self.icon_link, self.company_slug)

    def __repr__(self):
        return "%s %s %s %s" % (self.name, self.link, self.icon_link, self.company_slug)
