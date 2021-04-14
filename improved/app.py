from flask import Flask, render_template, request, session
# from src.Company import Company
# from src.Person import Person
# from src.prepare_data import prepare,get_options
from src.Manager import Manager

app = Flask(__name__)
manager = Manager()


@app.route('/<company_slug>/entries/show_all', methods=['POST'])
def show_all_signatures_of_company():
    pass


@app.route('/<company_slug>/<entry_id>/signature', methods=['POST'])
def show_signature_of_entry(company_slug, entry_id):
    entry = manager.get_entry_by_id(entry_id)
    template = company_slug + '/' + str(
        manager.get_template(company_slug)) + manager.SUFFIX_FOR_SINGLE_SIGNATURE_TEMPLATE + '.html'

    return render_template(template, data=entry, social_media=manager.get_social_media(company_slug))
    # return 'ssdazsd'


@app.route('/<company_slug>/entries', methods=['POST'])
def show_entries(company_slug):

    # print("slug = ", company_slug)
    entries = [x for x in manager.get_entries() if x.company_slug == company_slug]
    print(entries)
    return render_template('entries.html', entries=entries, company_slug=company_slug)


@app.route('/')
def index():
    return render_template('select_template.html', companies=manager.get_companies())


if __name__ == '__main__':
    app.run(debug=True)
