import json
import csv
import time

from src.Company import Company
from src.PersonEntry import PersonEntry
from src.SocialMedia import SocialMedia
from src.Database import Database
from src.FlagIcon import FlagIcon

from phone_iso3166.country import *


class Manager:
    SETTINGS_FILE_PATH = "data/settings.json"
    DATA_FILE_PATH = "data/__data.csv"

    # SUFFIX_FOR_SINGLE_SIGNATURE_TEMPLATE = '-single'
    # SUFFIX_FOR_ALL_SIGNATURES_TEMPLATE = '-all'
    def __init__(self):
        self.__database = Database()

        # self.__read_settings()  # read first
        # self.ENTRIES = self.__read_data()

    def get_entry_by_id(self, id_: int):
        return self.__database.get_entry_by_id(id_)

    # construct template path
    def get_template(self, company_slug: str):
        template = company_slug + '/' + str(
            self.__database.get_template(company_slug)) + '.html'
        return template

    def get_social_media(self, company_slug) -> {}:
        social_media = self.__database.get_social_media_by_company(company_slug)

        social_media_dict = {}
        for s in social_media:
            social_media_dict[s.name] = s

        # example:
        # obj = social_media['facebook'] -> returns the object - SocialMedia()
        # obj.link ... - access object

        return social_media_dict

    def get_companies(self) -> []:
        return self.__database.get_companies()

    def get_entries(self) -> []:
        return self.ENTRIES

    def initialize_setting(self):
        reload_settings = False
        if reload_settings:
            self.__read_settings()
            self.__read_data()
        else:
            pass
        # if path.exists(self.SETTINGS_FILE_PATH):
        #     self.__read_settings()
        #     self.__read_data()
        # else:
        #     #             continue with current settings
        #     pass

    def __read_settings(self) -> []:
        data = []
        with open(Manager.SETTINGS_FILE_PATH) as f:
            data = json.load(f)

        if not data:
            return []

        self.flag_icons = data['country_icons']
        companies_info = data['companies-info']

        for company_name in companies_info:
            company = companies_info[company_name]

            social_media = self.__set_up_social_media(company['social_links'], company['social_icons'], company['slug'])
            c = Company(company_name, company['slug'], company['template_name'], social_media)

            self.__set_up_company_info(c)

    # def __read_settings(self) -> []:
    #     data = []
    #     with open(Manager.SETTINGS_FILE_PATH) as f:
    #         data = json.load(f)
    #
    #     self.flag_icons = data['country_icons']
    #     companies_info = data['companies-info']
    #     companies = []
    #     for company_name in companies_info:
    #         company = companies_info[company_name]
    #
    #         social_media = self.__set_up_social_links(company['social_links'], company['social_icons'])
    #         # print(social_media)
    #         # print(social_media['facebook'])
    #         c = Company(company_name, company['slug'], company['template_name'], social_media)
    #         companies.append(c)
    #
    #     self.COMPANIES = companies

    def __set_up_company_info(self, c):
        successful = self.__database.add_company(c)

        if successful:
            print("Company info added to db: ", c)
        else:
            print("Error adding company info to db: ", c)
        return successful

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
                    # check if data file has entry data inside
                    if len(row) > 0:
                        p = PersonEntry(
                            _id=row[0].strip(),
                            _name=row[1].strip(),
                            _alt_name=row[2].strip(),
                            _role=row[3].strip(),
                            _email=row[4].strip(),
                            _email2=row[5].strip(),
                            _mob1=row[6].strip(),
                            _mob2=row[7].strip(),
                            _work_num=row[8].strip(),
                            _company_name=row[9].strip(),
                            _nickname=row[10].strip(),
                            _website=row[11].strip(),
                            _website2=row[12].strip(),
                            _company_slug=row[13].strip()
                        )
                        # print(p)
                        # print(phone_country(p.mob1))
                        try:
                            p.mob1_flag_icon_link = self.flag_icons[phone_country(p.mob1)]
                            p.mob2_flag_icon_link = self.flag_icons[phone_country(p.mob2)] if p.mob2 else ""
                        except:
                            p.mob1_flag_icon_link = ''
                            p.mob2_flag_icon_link = ''

                        self.__database.add_new_entry(p)
                        # people.append(p)

                    else:
                        pass

                line_count += 1
        return people

    def __set_up_social_media(self, social_links: {}, social_icons: {}, company_slug: str):
        # self.__database = DatabaseClass()
        successful = False
        for i in social_links:
            sm = SocialMedia(i, social_links[i], social_icons[i], company_slug)

            successful = self.__database.add_social_media(sm)
            if successful:
                print('Social media added for', company_slug)
            else:
                print('Error when adding Social media for', company_slug)

        return successful

    # def add_entry_to_data(self, p: PersonEntry):
    #     id_ = -1
    #     with open(Manager.DATA_FILE_PATH) as csv_file:
    #         csv_reader = csv.reader(csv_file, delimiter=',')
    #         line_count = 0
    #         for row in csv_reader:
    #             # print(row)
    #             # print()
    #             if line_count == 0:
    #                 pass
    #             else:
    #                 id_ = int(row[0]) if len(row) > 0 else 0
    #
    #             line_count += 1
    #         csv_file.close()
    #     id_ += 1
    #     with open(self.DATA_FILE_PATH, 'a', newline='') as file:
    #         fieldnames = ['id', 'name', 'alt_name', 'role', 'email', 'email2', 'mob1', 'mob2', 'work_num',
    #                       'company_name', 'Nickname', 'website', 'website2', 'company_slug']
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #
    #         writer.writerow({'id': id_, 'name': p.name,
    #                          'alt_name': p.alt_name, 'role': p.role,
    #                          'email': p.email, 'email2': p.email2, 'mob1': p.mob1, 'mob2': p.mob2,
    #                          'work_num': p.work_num, 'company_name': p.company_name,
    #                          'Nickname': p.nickname, 'website': p.website,
    #                          'website2': p.website2, 'company_slug': p.company_slug})
    #
    #     # update current data lists
    #     self.update()

    def get_entry_by_id_from_company(self, company_slug, entry_id) -> PersonEntry:
        return self.__database.get_entry_by_id_from_slug(entry_id, company_slug)

    def update_entry(self, updated_data: {}, company_slug: str, entry_id):
        entry = self.__database.get_entry_by_id_from_slug(entry_id, company_slug)
        entry.name = updated_data['name']
        entry.alt_name = updated_data['alt_name']
        entry.role = updated_data['role']
        entry.email = updated_data['email']
        entry.email2 = updated_data['email2']
        entry.mob1 = updated_data['mob1']
        entry.mob2 = updated_data['mob2']
        entry.work_num = updated_data['work_num']
        # p.company_name = updated_data['company_name']
        entry.nickname = updated_data['nickname']
        entry.website = updated_data['website']
        entry.website2 = updated_data['website2']
        # p.company_slug = updated_data['company_slug']
        return self.__database.update_entry(entry_id, company_slug, updated_entry=entry)

        #
        #     self.replace_entry_to_data(p)
        #     return True
        # else:
        #     return False

    # def replace_entry_to_data(self, p: PersonEntry, ):
    #
    #     tempfile = NamedTemporaryFile(mode='w', delete=False)
    #
    #     fieldnames = ['id', 'name', 'alt_name', 'role', 'email', 'email2', 'mob1', 'mob2', 'work_num',
    #                   'company_name', 'nickname', 'website', 'website2', 'company_slug']
    #
    #     with open(self.DATA_FILE_PATH, 'r') as csvfile, tempfile:
    #         reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    #         writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
    #         for row in reader:
    #             if str(row['id']) == str(p.id):
    #                 print('updating row', row['id'])
    #                 for rf in fieldnames:
    #                     print('RF::', rf)
    #                     row[rf] = p.to_dict()[rf]
    #
    #             #     row['Name'], row['Course'], row['Year'] = stud_name, stud_course, stud_year
    #             # row = {'ID': row['ID'], 'Name': row['Name'], 'Course': row['Course'], 'Year': row['Year']}
    #             # writer.writerow(row)
    #
    #     shutil.move(tempfile.name, self.DATA_FILE_PATH)
    #     ######
    #     # with open(self.DATA_FILE_PATH, 'a', newline='') as file:
    #     #     fieldnames = ['id', 'name', 'alt_name', 'role', 'email', 'email2', 'mob1', 'mob2', 'work_num',
    #     #                   'company_name', 'Nickname', 'website', 'website2', 'company_slug']
    #     #     writer = csv.DictWriter(file, fieldnames=fieldnames)
    #
    #     #     writer.writerow({'id': id_, 'name': p.name,
    #     #                      'alt_name': p.alt_name, 'role': p.role,
    #     #                      'email': p.email, 'email2': p.email2, 'mob1': p.mob1, 'mob2': p.mob2,
    #     #                      'work_num': p.work_num, 'company_name': p.company_name,
    #     #                      'Nickname': p.nickname, 'website': p.website,
    #     #                      'website2': p.website2, 'company_slug': p.company_slug})

    # def update(self):
    #     # re-read data
    #     # check if an entry is added from the app, update the current list of entries
    #     self.__read_data()

    def get_entries_by_slug(self, company_slug):
        return self.__database.get_entries_by_slug(company_slug)

    def get_existing_company_slugs(self) -> []:
        return self.__database.get_existing_company_slugs()

    def get_flag_icon(self, mob) -> FlagIcon:
        country = phone_country(mob)
        print('COUNTRY:::', country)
        return self.__database.get_flag_icon(country)

    def add_new_entry(self, p) -> bool:
        return self.__database.add_new_entry(p)

    def delete_entry_by_id_from_slug(self, entry_id: int, company_slug: str) -> bool:
        return self.__database.delete_entry_by_id_from_slug(entry_id, company_slug)
