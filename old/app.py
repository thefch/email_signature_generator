from flask import Flask, render_template,request,session
from src.Company import Company
from src.Person import Person
from src.prepare_data import prepare,get_options
app = Flask(__name__)
 
# GRIZZLY_TEMPLATE_NAME='grizzly'
# MONARCH_TEMPLATE_NAME='monarch'
# MONARCH_TEMPLATE_NAME='threemushrooms'

# CURRENT_TEMPLATE_NAME=''




@app.route('/show_all',methods=['POST'])
def show_all():
    try:
        t = request.form['template'].lower()
    except:
        return "Error please try again!"

    # init data
    template = Company.determine_template(t)

    # get company enum class
    company = Company.get_company(template)

    # get the path of template
    data,template_path = prepare(template,company,True)
    print('TEMPLATE PATH::',template_path)

    # file_path = get_template_path(company,True)
    
    return render_template(template_path,entries=data)

@app.route('/user', methods=['POST'])
def user():
    try:
        n = request.form['name']
        t = request.form['template'].lower()
    except:
        return "Error please try again!"
    
    template = Company.determine_template(t)
    company = Company.get_company(template)
    
    data,file_path = prepare(template,company,False,n)

    # file_path = get_template_path(company,False)


    if data:
        return render_template(file_path,data=data)
    else:
        return "No such name found!"

@app.route('/')
def option():
    return render_template('option.html',options=get_options())

@app.route('/index',methods=['POST'])
def index():
    option = None
    try:
        option = request.form['option']
    except Exception:
        return "Error!!"

    selected = Company.determine_template(option)

    data,_ = prepare(selected,None,False)

    return render_template(
        "start.html",
        entries=data,
        option=option
        )

if __name__ == '__main__':
    app.run(debug=True)


