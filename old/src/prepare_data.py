import enum
import json
from src.Company import Company
from src.Person import Person
import csv

# set all the names for the tempaltes
# make sure that the name is included, 'templates' is just to make sense
OPTIONS = ["Grizzly Templates", 'Monarch Templates', 'ThreeMushrooms Templates']

# data and settings file paths
SETTINGS_FILE_PATH="data/settings.json"
DATA_FILE_PATH = 'data/data.csv'


def get_options():
    return OPTIONS

def get_template_path(option:Company,show_all:bool):
    with open(SETTINGS_FILE_PATH) as json_file:
        d = json.load(json_file)
        d=d['paths']
        
        if show_all:    
            return d[option]['many']
        else:
            return d[option]['one']
            
    

# load settings from file,
# links and template paths
def load_settings(template):
    settings = {}
    with open(SETTINGS_FILE_PATH) as json_file:
        d = json.load(json_file)
        d=d['links']
        for i in d[template]:
            settings[i]=d[template][i]
    return settings


# load data information from file
# create Person objects
def load_data(settings,template,name):
    data = []
    
    # read the csv file with each person's data
    with open(DATA_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                p = Person( row[0].strip(),
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
                                row[14].strip(),
                                row[15].strip(),
                                row[16].strip(),
                                row[17].strip())
                p.add_link('facebook',settings['facebook'].strip(),)
                p.add_link('twitter',settings['twitter'].strip())
                p.add_link('instagram',settings['instagram'].strip())
                p.add_link('linkedin',settings['linkedin'].strip())
                p.add_link('youtube',settings['youtube'].strip())
                p.add_link('website',settings['website'].strip())
                
                if template is None:
                    data.append(p)
                
                elif template == row[17]:
                    if name is not None:
                        if row[0].lower()==name.lower().strip():
                            return p
                    else:
                        # print("Name:{} ,Role:{} ,Email:{} ,Office_address:{} ,Post_code:{} ,Country:{}, cy_mob:{}, us_mob:{}, bh_mob:{} , Company_name:{}, IGN:{}"
                        # .format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
                        data.append(p)
            line_count += 1
        print(f'Processed {line_count} lines.')
        
    return data
        
# prepare all the data from csv and json
# input first name or the whole name if one person is required
def prepare(template:str,company:Company,show_all:bool,name=None):

    # read settings first to init the dictionary with links
    settings = load_settings(template)
    data = load_data(settings,template,name)
    template_path = get_template_path(template,show_all)
    
    return data,template_path