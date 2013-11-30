#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
from qs import questions

myform=cgi.FieldStorage()
cgitb.enable()
cursor = MySQLdb.connect(host="localhost",user="askerry",passwd="password",db="aesbehave").cursor()
print 'Content-type:text/html\n\n'

#cgitb.enable(display=0, logdir="/path/to/logdir")

theids=myform.keys()
#print "<p>these are the ids: %s </p>" %(theids)
qnums=[]
qnumber=0
for q in questions:
	qnumber=qnumber+1
	qnums.append(str(qnumber))
shuffle(qnums) 
qindex=myform['qindex'].value
qindex=int(qindex)
### css setup
print '''
<head><title>Research Study</title>

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
<style type="text/css" media="all">@import "css/style.css";</style>

<script>
function validate(form){
    if (!checkTextField(form.subjid)) {alert('Please enter the correct ID!');return false;} 
}

function checkTextField(textField){
    if (textField.value!='') return true;
    return false;
}
</script>

</head>
'''

print '''
<html>
<head><title>Research Study: Welcome!</title>

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

<style type="text/css">
    body {
        font-family:verdana,arial,helvetica,sans-serif;
        font-size:100%;
    }
    #container {
        width:550px;
        margin:40px auto;
    }
    #verbcontainer {
        width:550px;
        margin:40px auto;
    }
    </style>

<p style="text-align:center"><font size="5"><br><br> <b>Hello! Thank you for signing up to do our study!</font></p></b>

<p style="text-align:left;margin-left:20px;margin-right:20px"><font size="4">
instruct line 1
<br><br>
instruct line 2
<br><br>
instruct line 3
<br><br>
<b> if you accept these conditions and are ready to begin, please fill in your username and click below </b>
<br><br>
</div>
</body>
</html>
'''


####end of setup
qindex=str(qindex)
qnumlist=qnums[0]
count=0
for q in qnums:
	count=count+1
	if count<len(qnums):
		qnumlist=qnumlist+','+qnums[count]
#print "<p>these are the new qnums: %s </p>" %(qnumlist)
 
print '''
<div id="page_content" align="center";  margin-left: 160px;">
<form name="myform" action="question.py" method="submit" onSubmit="return validate(myform)">
<input type="text" name="subjid">
<br>
<input type="hidden" name="qindex" value="'''+qindex+'''">
<input type="hidden" name="qnums" value="'''+qnumlist+'''">
<input type="submit" value="Continue" /></center>
<br><br><br><br>
</form>
</div>
</body>
</html>
'''
#end

