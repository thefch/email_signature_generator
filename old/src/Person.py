class Person():
    def __init__(self,_name,_alt_name,_role,_email,_email2,_office_address,_city,_post_code,_country,
    _cy_mob,_us_mob,_bh_mob,_work_num,_company_name,_nickname,_website,_website2,_company_tag):
        self.name = _name
        self.alt_name = _alt_name
        self.role = _role
        self.email= _email
        self.email2 = _email2
        self.office_address = _office_address
        self.city=_city
        self.post_code=_post_code
        self.country=_country
        self.cy_mob=_cy_mob
        self.us_mob=_us_mob
        self.bh_mob=_bh_mob
        self.work_num=_work_num
        self.company_name=_company_name
        self.nickname=_nickname
        self.website=_website
        self.website2=_website2
        self.company_tag = _company_tag
        self.links = {}

    def __str__(self):
        return "{} {} {} {}".format(self.name,self.role,self.cy_mob,self.company_name)

    def add_link(self,n,link):
        self.links[n]=link