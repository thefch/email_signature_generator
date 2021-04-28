import os
import sqlite3
from sqlite3 import Error

from src.PersonEntry import PersonEntry
from src.SocialMedia import SocialMedia
from src.Company import Company
from src.FlagIcon import FlagIcon

# if path does not work use this one:
PATH = "data/db.sqlite"


class Database:
    def __init__(self):
        self.connect()
        # pass

    @staticmethod
    def connect():
        conn = None
        try:
            if os.path.exists(PATH):
                conn = sqlite3.connect(PATH)
                # print('Connectd to db:', db, '  Successfully!')
            else:
                print("Could not connect to Database: NOT FOUND!")
        except Error as e:
            print(e)

        return conn

    def add_social_media(self, sm) -> bool:
        conn = self.connect()
        cursor = conn.cursor()

        query = """INSERT INTO social_media_tb ('name','link','icon_link','company_slug')
                    VALUES(?,?,?,?);"""

        args = (sm.name, sm.link, sm.icon_link, sm.company_slug)

        try:
            cursor.execute(query, args)
            conn.commit()
            print("SocialMedia added to db: ", sm)
            cursor.close()
            conn.close()

            return True
        except Exception as err:
            print(err)

        cursor.close()
        conn.close()

        return False

    def add_company(self, c: Company):
        conn = self.connect()
        cursor = conn.cursor()

        query = """INSERT INTO company_tb ('name','slug','template_name')
                            VALUES(?,?,?);"""

        args = (c.name, c.slug, c.template_name)

        try:
            cursor.execute(query, args)
            conn.commit()
            print("Company info added to db: ", c)
            cursor.close()
            conn.close()

            return True
        except Exception as err:
            print(err)

        cursor.close()
        conn.close()

        return False

    def add_new_entry(self, p: PersonEntry) -> bool:
        conn = self.connect()
        cursor = conn.cursor()

        query = """INSERT INTO entries_tb ('name','alt_name','role','email','email2','mob1','mob2','work_num',
        'company_name','nickname','website','website2','company_slug','mob1_flag_icon_link','mob2_flag_icon_link')
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

        args = (
            p.name, p.alt_name, p.role, p.email, p.email2, p.mob1, p.mob2, p.work_num, p.company_name, p.nickname,
            p.website, p.website2, p.company_slug, p.mob1_flag_icon_link, p.mob2_flag_icon_link)

        try:
            cursor.execute(query, args)
            conn.commit()
            print("Entry info added to db: ", p)
            cursor.close()
            conn.close()

            return True
        except Exception as err:
            print(err)

        cursor.close()
        conn.close()

        return False

    def get_companies(self) -> []:
        con = self.connect()
        cur = con.cursor()
        query = """
                   SELECT * FROM company_tb;       
                   """

        companies = []
        try:
            cur.execute(query)
            comps = cur.fetchall()

            # double check if is not None
            if comps is not None:
                for i in comps:
                    c = Company(name_=i[0], slug_=i[1], template_name_=i[2])
                    companies.append(c)
        except Error as err:
            raise err

        cur.close()
        con.close()
        return companies

    def get_entries_by_slug(self, company_slug: str):
        con = self.connect()
        cur = con.cursor()
        query = """
                   SELECT * FROM entries_tb WHERE company_slug=?
                   """
        args = (company_slug,)

        entries = []
        try:
            cur.execute(query, args)
            entries_temp = cur.fetchall()

            # double check if is not None
            if entries_temp is not None:
                for i in entries_temp:
                    p = PersonEntry(
                        _id=i[0],
                        _name=i[1].strip(),
                        _alt_name=i[2].strip(),
                        _role=i[3].strip(),
                        _email=i[4].strip(),
                        _email2=i[5].strip(),
                        _mob1=i[6].strip(),
                        _mob2=i[7].strip(),
                        _work_num=i[8].strip(),
                        _company_name=i[9].strip(),
                        _nickname=i[10].strip(),
                        _website=i[11].strip(),
                        _website2=i[12].strip(),
                        _company_slug=i[13].strip(),
                        _mob1_flag_icon_link=i[14].strip(),
                        _mob2_flag_icon_link=i[15].strip()
                    )
                    entries.append(p)
        except Error as err:
            raise err

        cur.close()
        con.close()
        return entries

    def get_template(self, company_slug) -> str:
        con = self.connect()
        cur = con.cursor()
        query = """
               SELECT * FROM company_tb WHERE slug=?
               """
        args = (company_slug,)

        comp_template = ''
        try:
            cur.execute(query, args)
            comp = cur.fetchone()

            # double check if is not None
            if comp is not None:
                comp_template = comp[2]
        except Error as err:
            raise err

        cur.close()
        con.close()
        return comp_template

    def get_social_media_by_company(self, company_slug) -> [SocialMedia]:
        con = self.connect()
        cur = con.cursor()
        query = """
               SELECT * FROM social_media_tb WHERE company_slug=?
               """
        args = (company_slug,)

        social_media = []
        try:
            cur.execute(query, args)
            social_media_temp = cur.fetchall()

            # double check if is not None
            if social_media_temp is not None:
                for i in social_media_temp:
                    s = SocialMedia(
                        name_=i[0],
                        social_link_=i[1],
                        social_icon_=i[2],
                        company_slug_=i[3])
                    social_media.append(s)
        except Error as err:
            raise err

        cur.close()
        con.close()
        return social_media

    def get_entry_by_id(self, id_) -> PersonEntry:
        con = self.connect()
        cur = con.cursor()
        query = """
                       SELECT * FROM entries_tb WHERE id=?
                       """
        args = (id_,)

        entry = None
        try:
            cur.execute(query, args)
            entry_temp = cur.fetchone()

            # double check if is not None
            if entry_temp is not None:
                entry = PersonEntry(
                    _id=entry_temp[0],
                    _name=entry_temp[1].strip(),
                    _alt_name=entry_temp[2].strip(),
                    _role=entry_temp[3].strip(),
                    _email=entry_temp[4].strip(),
                    _email2=entry_temp[5].strip(),
                    _mob1=entry_temp[6].strip(),
                    _mob2=entry_temp[7].strip(),
                    _work_num=entry_temp[8].strip(),
                    _company_name=entry_temp[9].strip(),
                    _nickname=entry_temp[10].strip(),
                    _website=entry_temp[11].strip(),
                    _website2=entry_temp[12].strip(),
                    _company_slug=entry_temp[13].strip(),
                    _mob1_flag_icon_link=entry_temp[14].strip(),
                    _mob2_flag_icon_link=entry_temp[15].strip()
                )
        except Error as err:
            raise err

        cur.close()
        con.close()
        return entry

    def get_entry_by_id_from_slug(self, entry_id, company_slug) -> PersonEntry:
        con = self.connect()
        cur = con.cursor()
        query = """
                SELECT * FROM entries_tb WHERE id=? AND company_slug=?
                """
        args = (entry_id, company_slug)

        entry = None
        try:
            cur.execute(query, args)
            entry_temp = cur.fetchone()

            # double check if is not None
            if entry_temp is not None:
                entry = PersonEntry(
                    _id=entry_temp[0],
                    _name=entry_temp[1].strip(),
                    _alt_name=entry_temp[2].strip(),
                    _role=entry_temp[3].strip(),
                    _email=entry_temp[4].strip(),
                    _email2=entry_temp[5].strip(),
                    _mob1=entry_temp[6].strip(),
                    _mob2=entry_temp[7].strip(),
                    _work_num=entry_temp[8].strip(),
                    _company_name=entry_temp[9].strip(),
                    _nickname=entry_temp[10].strip(),
                    _website=entry_temp[11].strip(),
                    _website2=entry_temp[12].strip(),
                    _company_slug=entry_temp[13].strip(),
                    _mob1_flag_icon_link=entry_temp[14].strip(),
                    _mob2_flag_icon_link=entry_temp[15].strip()
                )
        except Error as err:
            raise err

        cur.close()
        con.close()
        return entry

    def get_existing_company_slugs(self):
        con = self.connect()
        cur = con.cursor()
        query = """
                      SELECT * FROM company_tb
                      """

        company_slugs = []
        try:
            cur.execute(query)
            companies_temp = cur.fetchall()

            # double check if is not None
            if companies_temp is not None:
                for i in companies_temp:
                    company_slugs.append(i[1])
        except Error as err:
            raise err

        cur.close()
        con.close()
        return company_slugs

    def update_entry(self, entry_id, company_slug, updated_entry=None) -> [bool, PersonEntry]:
        con = self.connect()
        cur = con.cursor()
        query = """
                UPDATE entries_tb 
                SET name=?,alt_name=?, role=?,email=?,email2=?,mob1=?,mob2=?,work_num=?,
                   nickname=?,website=?,website2=?
                WHERE id=? AND company_slug=?
                """

        args = (
            updated_entry.name, updated_entry.alt_name, updated_entry.role, updated_entry.email, updated_entry.email2,
            updated_entry.mob1, updated_entry.mob2, updated_entry.work_num,
            updated_entry.nickname, updated_entry.website, updated_entry.website2,
            entry_id, company_slug)

        updated = False
        try:
            cur.execute(query, args)
            con.commit()
            print("Updated entry -> id:%s" % entry_id)

            updated = True
            updated_entry = self.get_entry_by_id(entry_id)
        except Error as err:
            print("Error updating entry -> id:%s" % entry_id)
            raise err

        cur.close()
        con.close()
        return updated, updated_entry

    def get_flag_icon(self, country: str) -> FlagIcon:
        con = self.connect()
        cur = con.cursor()
        query = """
              SELECT * FROM flag_icons_tb WHERE country_name=?
              """

        args = (country,)

        flag_icon = None
        try:
            cur.execute(query, args)
            flag_icon_temp = cur.fetchone()

            # double check if is not None
            if flag_icon_temp is not None:
                flag_icon = FlagIcon(country_name_=flag_icon_temp[1], link_=flag_icon_temp[2], id_=flag_icon_temp[0])

        except Error as err:
            raise err

        cur.close()
        con.close()
        return flag_icon

    def delete_entry_by_id_from_slug(self, entry_id:int, company_slug:str) -> bool:
        conn = self.connect()
        cursor = conn.cursor()

        query = """
                DELETE from entries_tb WHERE id=?
                """

        args = (entry_id,)

        successful = False
        try:
            cursor.execute(query, args)
            conn.commit()
            print("Entry deleted from db -> id:%s slug:%s" % (entry_id, company_slug))

            successful = True
        except Error as err:
            raise err

        cursor.close()
        conn.close()
        return successful


if __name__ == '__main__':
    PATH = '../data/db.sqlite'
    database = Database()
    database.delete_entry_by_id_from_slug(16, 'grizzly')
    print(database.get_flag_icon('US'))
    # database.test_SQL_sanitation()
    # database.create_test_users_clients(5)
