from flask import Flask, render_template, request, g
from generator import gen
import sqlite3


# FLASK app
app = Flask(__name__)


# DATABASE Utility Functions
DATABASE = 'db/marks.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Routing

@app.route('/')
def index():

	return "Homepage"

@app.route('/template/<name>')
def template(name):
	return render_template("template.html", name=name)


@app.route('/result/', methods=['GET', 'POST'])
def result():
	college = {}
	marks = []
	average = 0.0
	debug = ""
	if request.method == 'POST':
		college['code'] = request.form.get('college')
		sort = request.args.get('sort')
		order = request.args.get('order')
		if sort != "percentage" and sort != "name":
			sort = "rollno"
		like = "__" + college['code'][1:] + "%"
		#debug = sort
		if order == 'desc':
			marks = query_db("SELECT rollno, name, percentage FROM marks where rollno LIKE ? ORDER BY "+ sort +" DESC", [like])
		else:
			marks = query_db("SELECT rollno, name, percentage FROM marks where rollno LIKE ? ORDER BY " + sort, [like])
		for i in marks:
			average += float(i[2])
		if len(marks) > 0:
			average /= (len(marks) * 100)
		average = '{:.2%}'.format(average)
		return render_template('result.html', marks=marks, college=college, average=average, debug=debug)
	return render_template('result.html')


@app.route('/result/<int:rollno>')
def result_no(rollno):
	k = gen.btech_res(rollno)
	if not k:
		return "Invalid URL"
	t, name = k
	x = []
	if len(t) > 1:
		total = 0.0
		mtotal = 0.0
		for i in t:
			x.append(i[:3])
			total += int(i[1])
			mtotal += int(i[2])
		x.append(['Total', str(int(total)), str(int(mtotal))])
		percentage = '{:.2%}'.format(total/mtotal)
	elif len(t) == 1:
		x.append(t[0])
	else:
		x.append("Some Error Occured")
	return render_template('marks.html', marks=x, name=name.title(), percentage=percentage)


@app.route('/result2/<int:rollno>')
def result2_no(rollno):
	t, name = gen.btech_res(rollno)
	x = []
	if len(t) > 1:
		total = 0.0
		mtotal = 0.0
		for i in t:
			i[0] = '{:->5}'.format(i[0])
			x.append(i[0] + " - " + i[1] + "/" + i[2])
			total += int(i[1])
			mtotal += int(i[2])
		x.append('{:->5}'.format('Total') + " - " + str(int(total)) + "/" + str(int(mtotal)))
		x.append('Percentage: {:.2%}'.format(total/mtotal))
	elif len(t) == 1:
		x.append(t[0])
	else:
		x.append("Some Error Occured")
	return render_template('marks2.html', marks=x, name=name.title())

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=False)
