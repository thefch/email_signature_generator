class Person():
    def __init__(self, _id, _name, _alt_name, _role, _email, _email2,
                 _mob1, _mob2, _work_num, _company_name,
                 _nickname, _website, _website2, _company_slug):
        self.id = _id
        self.name = _name
        self.alt_name = _alt_name
        self.role = _role
        self.email = _email
        self.email2 = _email2
        self.mob1 = _mob1
        self.mob2 = _mob2
        self.work_num = _work_num
        self.company_name = _company_name
        self.nickname = _nickname
        self.website = _website
        self.website2 = _website2
        self.company_slug = _company_slug

    def __str__(self):
        return "{} {} {} {}".format(self.name, self.role, self.mob1, self.company_name)

    def __repr__(self):
        return "{} {} {} {}".format(self.name, self.role, self.mob1, self.company_name)
