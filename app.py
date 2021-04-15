from flask import Flask, render_template, request, redirect, url_for

from src.Manager import Manager
from src.Person import Person

app = Flask(__name__)
manager = Manager()


@app.route('/<company_slug>/entries/show_all', methods=['POST'])
def show_all_signatures_of_company(company_slug):
    entries = [x for x in manager.get_entries() if x.company_slug == company_slug]
    template = company_slug + '/' + str(
        manager.get_template(company_slug)) + '.html'

    return render_template(template, entries=entries, social_media=manager.get_social_media(company_slug))


@app.route('/<company_slug>/<entry_id>/signature', methods=['POST'])
def show_signature_of_entry(company_slug, entry_id):
    entry = manager.get_entry_by_id(entry_id)
    template = company_slug + '/' + str(
        manager.get_template(company_slug)) + '.html'

    return render_template(template, entries=[entry], social_media=manager.get_social_media(company_slug))


@app.route('/<company_slug>/entries', methods=['POST', 'GET'])
def show_entries(company_slug):
    entries = [x for x in manager.get_entries() if x.company_slug == company_slug]
    return render_template('entries.html', entries=entries, company_slug=company_slug)


@app.route('/save_entry', methods=['POST'])
def save_entry():
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
        company_name = request.form['CompanyName']
        nickname = request.form['Nickname']
        primary_website = request.form['Website']
        secondary_website = request.form['Website2']
        company_slug = request.form['CompanySlug']
        read_successful = True
    except:
        pass

    if read_successful:
        p = Person(_name=name, _alt_name=alt_name, _role=role,
                   _email=primary_email_address, _email2=secondary_email_address,
                   _mob1=primary_number, _mob2=secondary_number, _work_num=work_number,
                   _company_name=company_name, _nickname=nickname, _website=primary_website,
                   _website2=secondary_website, _company_slug=company_slug)
        manager.add_entry_to_data(p)
        resp = redirect(url_for('show_entries', company_slug=company_slug))
    else:
        msg = "Error with creating a new entry"
        resp = redirect(url_for('index', msg=msg))
    return resp


@app.route('/add_entry', methods=['POST'])
def add_entry():
    return render_template('add_entry.html', companies=manager.COMPANIES)


@app.route('/')
def index():
    msg = ''
    try:
        msg = request.args.get('msg')
    except:
        msg = ''
    return render_template('select_template.html', msg=msg, companies=manager.get_companies())


@app.route('/manage')
def manage():
    return render_template('manage.html')


if __name__ == '__main__':
    app.run(debug=True)
