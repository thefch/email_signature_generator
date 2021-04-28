class FlagIcon:

    def __init__(self, country_name_: str, link_: str, id_=None):
        self.country_name = country_name_
        self.link = link_
        self.id = id_

    def __str__(self):
        return "%s %s " % (self.country_name, self.link)

    def __repr__(self):
        return "%s %s " % (self.country_name, self.link)