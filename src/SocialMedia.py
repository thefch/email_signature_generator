class SocialMedia:
    def __init__(self, name_, social_link_, social_icon_):
        self.name = name_
        self.link = social_link_
        self.icon_link = social_icon_

    def __str__(self):
        return "%s %s %s" % (self.name, self.link, self.icon_link)

    def __repr__(self):
        return "%s %s %s" % (self.name, self.link, self.icon_link)
