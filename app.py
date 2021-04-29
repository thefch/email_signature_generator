import time

from flask import Flask, render_template, request, redirect, url_for

from src.Manager import Manager
from src.PersonEntry import PersonEntry

app = Flask(__name__)
manager = Manager()


@app.route('/<company_slug>/update_entry/<entry_id>/delete', methods=['POST'])
def delete_entry(company_slug, entry_id):
    deleted = manager.delete_entry_by_id_from_slug(int(entry_id), company_slug)
    if deleted:
        msg = "Entry deleted id:%s from %s" % (entry_id, company_slug)
    else:
        msg = "Error deleting entry %s from %s" % (entry_id, company_slug)

    return redirect(url_for('index', msg=msg))


@app.route('/<company_slug>/update_entry/<entry_id>', methods=['POST'])
def update_entry(company_slug, entry_id):
    name = alt_name = role = primary_email_address = secondary_email_address = primary_number = secondary_number = \
        work_number = nickname = primary_website = secondary_website = ''

    read_from_form_successful = False
    try:
        name = request.form['FullName']
        alt_name = request.form['AltName']
        role = request.form['Role']
        primary_email_address = request.form['EmailAddress']
        secondary_email_address = request.form['EmailAddress2']
        primary_number = request.form['PrimaryNum']
        secondary_number = request.form['SecondaryNum']
        work_number = request.form['WorkNum']
        # company_name = request.form['CompanyName']
        nickname = request.form['Nickname']
        primary_website = request.form['Website']
        secondary_website = request.form['Website2']
        # new_company_slug = request.form['CompanySlug']
        read_from_form_successful = True
    except:
        pass

    if read_from_form_successful:
        updated_data = {'name': name, 'alt_name': alt_name, 'role': role,
                        'email': primary_email_address, 'email2': secondary_email_address,
                        'mob1': primary_number, 'mob2': secondary_number, 'work_num': work_number,
                        'nickname': nickname, 'website': primary_website,
                        'website2': secondary_website}
        manager.update_entry(updated_data, company_slug, entry_id)
        msg = "Successfully updated the signature"
        resp = redirect(url_for('show_signature_of_entry', company_slug=company_slug, entry_id=entry_id, msg=msg))
    else:
        msg = "Error updating the signature"
        resp = redirect(url_for('show_signature_of_entry', company_slug=company_slug, entry_id=entry_id, msg=msg))
    return resp


@app.route('/<company_slug>/edit_entry/<entry_id>', methods=['POST'])
def edit_entry(company_slug, entry_id):
    entry = manager.get_entry_by_id_from_company(company_slug, entry_id)
    existing_slugs = manager.get_existing_company_slugs()

    if entry is None:
        msg = "Error with finding person with id %s in %s" % (entry_id, company_slug)
        return redirect(url_for('index', msg=msg))

    if existing_slugs is None:
        existing_slugs = []

    return render_template('edit_entry.html', entry=entry, company_slugs=existing_slugs)


@app.route('/<company_slug>/entries/show_all', methods=['POST'])
def show_all_signatures_of_company(company_slug):
    entries = manager.get_entries_by_slug(company_slug)
    template = manager.get_template(company_slug)
    social_media = manager.get_social_media(company_slug)
    return render_template(template, entries=entries, social_media=social_media)


@app.route('/<company_slug>/<entry_id>/signature', methods=['POST', 'GET'])
def show_signature_of_entry(company_slug, entry_id):
    msg = ''
    try:
        msg = request.args.get('msg')
    except:
        msg = None

    entry = manager.get_entry_by_id(entry_id)
    template = manager.get_template(company_slug)
    social_media = manager.get_social_media(company_slug)
    return render_template(template, entries=[entry], social_media=social_media, msg=msg)


@app.route('/<company_slug>/entries', methods=['POST', 'GET'])
def show_entries(company_slug):
    msg = ''
    try:
        msg = request.args.get('msg')
    except:
        msg = ''
    entries = manager.get_entries_by_slug(company_slug)
    return render_template('entries.html', entries=entries, company_slug=company_slug, msg=msg)


@app.route('/save_new_entry', methods=['POST'])
def save_new_entry():
    name = alt_name = role = primary_email_address = secondary_email_address = primary_number = secondary_number = \
        work_number = company_name = nickname = primary_website = secondary_website = company_slug = None

    read_successful = False
    try:
        name = request.form['FullName']
        alt_name = request.form['AltName']
        role = request.form['Role']
        primary_email_address = request.form['EmailAddress']
        secondary_email_address = request.form['EmailAddress2']
        primary_number = request.form['PrimaryNum']
        secondary_number = request.form['SecondaryNum']
        work_number = request.form['WorkNum']
        company_slug = request.form['CompanySlug']
        company_name = request.form['CompanyName']
        nickname = request.form['Nickname']
        primary_website = request.form['Website']
        secondary_website = request.form['Website2']
        read_successful = True
    except:
        pass

    if read_successful:
        mob1_flag = manager.get_flag_icon(primary_number).link if manager.get_flag_icon(
            primary_number) is not None else ''
        mob2_flag = manager.get_flag_icon(secondary_number).link if manager.get_flag_icon(
            secondary_number) is not None else ''

        p = PersonEntry(_name=name, _alt_name=alt_name, _role=role,
                        _email=primary_email_address, _email2=secondary_email_address,
                        _mob1=primary_number, _mob2=secondary_number, _work_num=work_number,
                        _company_name=company_name, _nickname=nickname, _website=primary_website,
                        _website2=secondary_website, _company_slug=company_slug, _mob1_flag_icon_link=mob1_flag,
                        _mob2_flag_icon_link=mob2_flag)

        print("PERSON:::", p)
        if manager.add_new_entry(p):
            msg = "Successfully added entry: %s" % p.name
            resp = redirect(url_for('show_entries', company_slug=company_slug, msg=msg))
        else:
            msg = "Error adding entry: %s" % p.name
            resp = redirect(url_for('index', msg=msg))
    else:
        msg = "Error with creating a new entry"
        resp = redirect(url_for('index', msg=msg))

    return resp


@app.route('/add_entry', methods=['POST'])
def add_entry():
    companies = manager.get_companies()
    return render_template('add_entry.html', companies=companies)


@app.route('/')
def index():
    msg = ''
    try:
        msg = request.args.get('msg')
    except:
        msg = ''
    return render_template('select_template.html', msg=msg, companies=manager.get_companies())


########################################################################################################################

@app.route('/manage', methods=['POST', 'GET'])
def manage():
    return render_template('manage.html')


@app.route('/add_new_company_slug', methods=['POST'])
def add_new_company_slug():
    return render_template('add_new_company_slug.html')


@app.route('/save_new_company_slug', methods=['POST'])
def save_new_company_slug():
    name = alt_name = role = primary_email_address = secondary_email_address = primary_number = secondary_number = \
        work_number = company_name = nickname = primary_website = secondary_website = company_slug = None

    read_successful = False
    try:
        company_name = request.form['CompanyName']
        company_slug = request.form['CompanySlug']
        template_name = request.form['TemplateName']
        facebook_link = request.form['FacebookLink']
        facebook_icon_link = request.form['FacebookIconLink']

        instagram_link = request.form['InstagramLink']
        instagram_icon_link = request.form['InstagramIconLink']

        twitter_link = request.form['TwitterLink']
        twitter_icon_link = request.form['TwitterIconLink']

        youtube_link = request.form['YoutubeLink']
        youtube_icon_link = request.form['YoutubeIconLink']

        linkedin_link = request.form['LinkedinLink']
        linkedin_icon_link = request.form['LinkedinIconLink']

        website_link = request.form['WebsiteLink']
        website_icon_link = request.form['WebsiteIconLink']

        read_successful = True
    except:
        pass
    return render_template('manage.html')


def main():
    # manager.initialize_setting()
    app.run(debug=True)


if __name__ == '__main__':
    main()
