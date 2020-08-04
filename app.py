from flask import Flask, render_template,request
import csv

app = Flask(__name__)


# prepare the data from csv
# input first name or the whole name
def prepare(name=None):
    data = []
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if name is not None:
                if row[0].lower()==name.lower().strip() or name.split()[0].lower().strip() in row[0].lower():
                    return {'name':row[0],
                            'role':row[1],
                            'email':row[2],
                            'address':row[3],
                            'post_code':row[4],
                            'country':row[5],
                            'cy_mob':row[6],
                            'us_mob':row[7],
                            'bh_mob':row[8],
                            'work_num':row[9],
                            'company_name':row[10],
                            'ign':row[11],
                            'website':row[12]
                            }

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print("Name:{} ,Role:{} ,Email:{} ,Office_address:{} ,Post_code:{} ,Country:{}, cy_mob:{}, us_mob:{}, bh_mob:{} , Company_name:{}, IGN:{}"
                # .format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
                data.append({'name':row[0],
                            'role':row[1],
                            'email':row[2],
                            'address':row[3],
                            'post_code':row[4],
                            'country':row[5],
                            'cy_mob':row[6],
                            'us_mob':row[7],
                            'bh_mob':row[8],
                            'work_num':row[9],
                            'company_name':row[10],
                            'ign':row[11],
                            'website':row[12]
                            })
                line_count += 1
            print()
        print(f'Processed {line_count} lines.')

    return data

@app.route('/show_all',methods=['POST','GET'])
def show_all():
    data = prepare()
    return render_template('template2all.html',entries=data)

@app.route('/user', methods=['POST','GET'])
def user():
    try:
        n = request.form['name']
    except:
        return "Error please try again!"
    
    data = prepare(n)
    if data:
        return render_template('template2.html',data=data)
    else:
        return "No such name found!"

@app.route('/')
def index():
    data = prepare()

    print('len:',len(data))
    return render_template(
        "start.html",
        entries=data
        )

if __name__ == '__main__':
    app.run(debug=True)
    # data = prepare()
    # if data:
    #     print("data found!!")

