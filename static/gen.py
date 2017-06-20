#!/usr/bin/python

import re
from mechanize import Browser
from bs4 import BeautifulSoup

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

            return marks_list
            # RETURN
    except:
        flag = False
        with open('res/marks.txt') as markslist:
                for line in markslist:
                        if rno in line:
                                flag = True
                                percentage = line.split(',')[-1]
                                # RETURN
                                break
        if not flag:
                print ("<h3>Some Problem Occured!!!</h3>")


rollno = input("Enter roll no.: ").strip()


def btech_res(rollno)
    if rollno:
        p_rollno = str(rollno)
        recfile = open("marks.txt", "U")
        rec = recfile.read()
        rec = rec.split("\n")
        
        for r in rec:
            row = r.split(',')
            if r and row[0] == p_rollno:
                return stud_rec(row[0], row[1])
                break
        recfile.close()
