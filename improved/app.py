from flask import Flask, render_template, request, session
# from src.Company import Company
# from src.Person import Person
# from src.prepare_data import prepare,get_options
from src.prepare_data import *

app = Flask(__name__)

SETTINGS_FILE_PATH = "data/settings.json"
DATA_FILE_PATH = "data/data.csv"
COMPANIES = []
ENTRIES = []


def get_entry_by_id(id: int):
    global ENTRIES
    for entry in ENTRIES:
        if entry.id == id:
            return entry
    return None


def get_template(company_slug: str):
    for c in COMPANIES:
        if c.slug == company_slug:
            return c.template_single_path
    return None


@app.route('/<company_slug>/entries/show_all', methods=['POST'])
def show_all_signatures_of_company():
    pass


@app.route('/<company_slug>/<entry_id>/signature', methods=['POST'])
def show_signature_of_entry(company_slug, entry_id):
    entry = get_entry_by_id(entry_id)
    template = get_template(company_slug) + '.html'
    return render_template(template, data=entry)


@app.route('/<company_slug>/entries', methods=['POST'])
def show_entries(company_slug):
    global ENTRIES
    ENTRIES = read_data(DATA_FILE_PATH)
    # print("slug = ", company_slug)
    entries = [x for x in ENTRIES if x.company_slug == company_slug]
    print(entries)
    return render_template('entries.html', entries=entries, company_slug=company_slug)


@app.route('/')
def index():
    global COMPANIES
    COMPANIES = read_settings(SETTINGS_FILE_PATH)
    return render_template('select_template.html', companies=COMPANIES)


if __name__ == '__main__':
    app.run(debug=True)
