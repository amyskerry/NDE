#!/usr/bin/python

#import the modules we need to run the script
import cgitb, cgi, MySQLdb, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
import datetime

#grab the form being passed in from the pervious script
form=cgi.FieldStorage()
cgitb.enable()

mydatabase="aesbehave"
mytable="demographics_tbl"

#log into the database
cursor = MySQLdb.connect(host="localhost",user="askerry",passwd="password",db="aesbehave").cursor()

datevar=datetime.datetime.now()
datevar=datevar.strftime("%Y-%m-%d %H:%M")

#grab the data stored in the form from the previous script
subjid = form['subjid'].value
formindex=form['rownum'].value
keycode=form['keycode'].value
age = form['age'].value
gender = form['gender'].value

#add the person to the database:  "insert" command for new rows

# store data onto server:  "update" commands to add data to existing row
cursor.execute('update demographics_tbl set age="'+age+'" where rownum="'+formindex+'"')
cursor.execute('update demographics_tbl set gender="'+gender+'" where rownum="'+formindex+'"')
cursor.execute('update demographics_tbl set submitdate="'+datevar+'" where rownum="'+formindex+'"')


for x in ['country','city','thoughts']:
    try:
        it = form[x].value
        cursor.execute('update demographics_tbl set '+x+'="'+it+'" where rownum="'+formindex+'"')
    except: pass


# display a thank you    
print 'Content-type:text/html\n\n'
print '''
<style type="text/css">
    body {
        font-family:verdana,arial,helvetica,sans-serif;
        font-size:100%;
    }
</style>
'''
print '''
<html>
<head><title>Research Study: Completed</title>

<body>
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
<style type="text/css" media="all">@import "css/drupalit.css";</style>
<style type="text/css" media="all">@import "css/content.css";</style>
<style type="text/css" media="all">@import "css/node.css";</style>
<style type="text/css" media="all">@import "css/defaults.css";</style>
<style type="text/css" media="all">@import "css/system.css";</style>
<style type="text/css" media="all">@import "css/userhttp://htmledit.squarefree.com/.css";</style>
<style type="text/css" media="all">@import "css/fieldgroup.css";</styl<style type="text/css" media="all">@import 

"css/date.css";</style>
<style type="text/css" media="all">@import "css/acidfree.css";</style>
<style type="text/css" media="all">@import "css/style.css";</style></head>
<div id="page_content" style="margin-right:160px;  margin-left: 160px;">

<br>
<p style="text-align:center"><font size="3"><b>You have finished our survey!</b> </p>
<p style="text-align:center"><font size="3">
Thank you very much for your participation.<br> Below is a code that you can enter into the Mechanical Turk start page in order to recieve your payment.  
<br><br>
'''
print "<b>Your keycode is: %s." % (keycode) 

print '''
<br>
</p>
<br>
</font>
</div>
<br><br>
</body>
</html>
'''
