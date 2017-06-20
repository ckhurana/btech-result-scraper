#!/usr/bin/python

import re
from threading import Thread
from mechanize import Browser
from bs4 import BeautifulSoup
import cgi
import cgitb

print ("Content-type:text/html")
print
print ("""<html>
	<head>
		<title>Avg Calculator</title>
		<link rel='stylesheet' href='style.css'><meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=0.8">
	</head>""")

cgitb.enable()

br = Browser()
# Ignore robots.txt
br.set_handle_robots(False)
br.set_handle_redirect(True)
br.addheaders = [('User-agent', 'Firefox')]

url = "http://duexam2.du.ac.in/RSLT_ND2016/Students/Combine_GradeCard.aspx"

# Parameters
p_type = 'Semester'
p_exam_flag = 'UG_SEMESTER_4Y'
p_stream = 'SC'
p_year = 'IV'
p_sem = 'VII'


def stud_rec(rno, name):
    try:
        br.open(url)

        p_colg = "0" + rno[2:4]
        p_course = rno[4:7]

        br.select_form('form1')
        br.form['ddlcollege'] = [p_colg, ]
        br.submit()

        br.select_form('form1')
        br.form['ddlexamtype'] = [p_type, ]
        br.submit()

        br.select_form('form1')
        br.form['ddlexamflag'] = [p_exam_flag, ]
        br.submit()

        br.select_form('form1')
        br.form['ddlstream'] = [p_stream, ]
        br.submit()

        br.select_form('form1')
        br.form['ddlcourse'] = [p_course, ]
        br.submit()

        br.select_form('form1')
        br.form['ddlpart'] = [p_year, ]
        br.submit()

        br.select_form('form1')
        br.form['ddlsem'] = [p_sem, ]

        br.form['txtrollno'] = rno
        br.form['txtname'] = name
        br.submit()
        htmltext = br.response()

        soup = BeautifulSoup(htmltext, "html.parser")
        marks_raw = soup.find_all(id="gvrslt")
        soup = BeautifulSoup(str(marks_raw[0]), "html.parser")
        marks_raw_list = soup.find_all("tr")
        marks_raw_list.pop(0)
        marks_list = []
        omarks = tmarks = 0.0

        if not marks_raw_list:
            print ("<h3>Record Not Found, Maybe!!!</h3>")
        else:
            for r in marks_raw_list:
                rw = re.findall('<td align="center">(.+?)</td>', str(r))
                marks_list.append(rw)
                omarks += float(rw[1])
                tmarks += float(rw[2])

            percentage = (omarks / tmarks) * 100.0
            print ("<h3>" + name + ": " + str(percentage) + "%</h3><hr>")
    except:
        print ("<script>console.log('Network Problem')</script>")
        flag = False
        with open('res/marks.txt') as markslist:
                for line in markslist:
                        if rno in line:
                                flag = True
                                percentage = line.split(',')[-1]
                                print ("<h3>" + name + ": " + str(percentage) + "%</h3><hr>")
                                break
        if not flag:
                print ("<h3>Some Problem Occured!!!</h3>")


print ("<body>")
print ("<h1>Average Calculator</h1><h3>B. Tech. C.S. - University of Delhi</h3><hr>")

form = cgi.FieldStorage()

is_rno_valid = False

if form.getfirst("rollno"):
    p_rollno = str(form.getfirst("rollno"))
    recfile = open("res/students_list.txt", "U")
    rec = recfile.read()
    rec = rec.split("\n")
    
    for r in rec:
        row = r.split(',')
        if r and row[1] == p_rollno:
            stud_rec(row[1], row[2])
            is_rno_valid = True
            break
    recfile.close()

if "rollno" in form and is_rno_valid == False:
    print ("<h3>Invalid or Incorrect Roll Number</h3><hr>")

print ('<form name="avgForm" method="post" action="index.py">')
print ('<p id="label">Roll Number:</p><p id="numError"></p><br><input type="text" name="rollno" placeholder="Enter roll number" maxlength="11" onchange="checknum()" onkeyup="checknum()"/>')
print ('<input type="submit" id="avgsubmit" value="Calculate" disabled=true/></form>')
print ("""<script>
	function checknum(){
		var num = document.forms.avgForm.rollno.value;
		if(isNaN(num)){
			document.getElementById("numError").style.display = "block";
			document.getElementById("numError").style.color = "red";
			document.getElementById("numError").innerHTML = "Roll Number should contain only numbers";
			document.getElementById("avgsubmit").disabled = true;
		}
		else
		if(num.length < 10){
			document.getElementById("numError").style.display = "block";
			document.getElementById("numError").innerHTML = "Roll Number should be 10 digits long";
			document.getElementById("numError").style.color = "red";
			document.getElementById("avgsubmit").disabled = true;
		} else {
			document.getElementById("numError").style.display = "none";
			document.getElementById("avgsubmit").disabled = false;
		}
	}
	</script>""")
print ("</body></html>")

