import json
import csv

from src.Company import Company
from src.Person import Person
from src.SocialMedia import SocialMedia
from phone_iso3166.country import *


class Manager:
    SETTINGS_FILE_PATH = "data/settings.json"
    DATA_FILE_PATH = "data/data.csv"
    # SUFFIX_FOR_SINGLE_SIGNATURE_TEMPLATE = '-single'
    # SUFFIX_FOR_ALL_SIGNATURES_TEMPLATE = '-all'

    def __init__(self):
        self.__read_settings()  # read first
        self.ENTRIES = self.__read_data()

    def get_entry_by_id(self, id_: int):
        for entry in self.ENTRIES:
            if entry.id == id_:
                return entry
        return None

    def get_template(self, company_slug: str):
        for c in self.COMPANIES:
            print(c)
            if c.slug == company_slug:
                return c.template_name
        return None

    def get_social_media(self, company_slug):
        for c in self.COMPANIES:
            if c.slug == company_slug:
                return c.social_media

    def get_companies(self) -> []:
        return self.COMPANIES

    def get_entries(self) -> []:
        return self.ENTRIES

    def __read_settings(self) -> []:
        data = []
        with open(Manager.SETTINGS_FILE_PATH) as f:
            data = json.load(f)

        self.flag_icons = data['country_icons']
        companies_info = data['companies-info']
        companies = []
        for company_name in companies_info:
            company = companies_info[company_name]

            social_media = self.__set_up_social_links(company['social_links'], company['social_icons'])
            # print(social_media)
            # print(social_media['facebook'])
            c = Company(company_name, company['slug'], company['template_name'], social_media)
            companies.append(c)

        self.COMPANIES = companies

    def __read_data(self):
        people = []

        with open(Manager.DATA_FILE_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # print(row)
                # print()
                if line_count == 0:
                    pass
                else:
                    p = Person(
                        row[1].strip(),
                        row[2].strip(),
                        row[3].strip(),
                        row[4].strip(),
                        row[5].strip(),
                        row[6].strip(),
                        row[7].strip(),
                        row[8].strip(),
                        row[9].strip(),
                        row[10].strip(),
                        row[11].strip(),
                        row[12].strip(),
                        row[13].strip(),
                        _id=row[0].strip())
                    # print(p)
                    # print(phone_country(p.mob1))
                    try:
                        p.mob1_flag_icon_link = self.flag_icons[phone_country(p.mob1)]
                        p.mob2_flag_icon_link = self.flag_icons[phone_country(p.mob2)] if p.mob2 else ""
                    except:
                        p.mob1_flag_icon_link = ''
                        p.mob2_flag_icon_link = ''

                    people.append(p)

                line_count += 1
        return people

    def __set_up_social_links(self, social_links, social_icons):
        social_media = {}
        for i in social_links:
            sm = SocialMedia(i, social_links[i], social_icons[i])
            # print(sm)
            social_media[i] = sm
        return social_media

    def add_entry_to_data(self, p: Person):
        id_ = -1
        with open(Manager.DATA_FILE_PATH) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # print(row)
                # print()
                if line_count == 0:
                    pass
                else:
                    id_ = int(row[0])
                line_count += 1
            csv_file.close()
        id_ += 1
        with open(self.DATA_FILE_PATH, 'a', newline='') as file:
            fieldnames = ['id', 'name', 'alt_name', 'role', 'email', 'email2', 'mob1', 'mob2', 'work_num',
                          'company_name', 'Nickname', 'website', 'website2', 'company_slug']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writerow({'id': id_, 'name': p.name,
                             'alt_name': p.alt_name, 'role': p.role,
                             'email': p.email, 'email2': p.email2, 'mob1': p.mob1, 'mob2': p.mob2,
                             'work_num': p.work_num, 'company_name': p.company_name,
                             'Nickname': p.nickname, 'website': p.website,
                             'website2': p.website2, 'company_slug': p.company_slug})

        # update current data lists
        self.update()

    def update(self):
        # re-read data
        # check if an entry is added from the app, update the current list of entries
        self.__read_data()
