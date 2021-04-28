class Company:

    def __init__(self, name_: str, slug_: str, template_name_: str):
        self.name = name_
        self.slug = slug_
        self.template_name = template_name_

    def __str__(self):
        return "%s %s" % (self.name, self.slug)

    def __repr__(self):
        return "%s %s" % (self.name, self.slug)
