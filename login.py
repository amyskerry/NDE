#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
from qs import questions, blacklist

myform=cgi.FieldStorage()
cgitb.enable()
cursor = MySQLdb.connect(host="localhost",user="askerry",passwd="password",db="aesbehave").cursor()
print 'Content-type:text/html\n\n'

#cgitb.enable(display=0, logdir="/path/to/logdir")

theids=myform.keys()
#print "<p>these are the ids: %s </p>" %(theids)
qnums=[]
for qn, q in enumerate(questions):
	if qn!=85 and qn !=86:#these are the check questions
		qnums.append(str(qn+1))
for bl in blacklist:
	blnum=bl[1:]
	qnums.remove(blnum)
shuffle(qnums)
qnums.insert(6,str(86))
qnums.insert(16,str(87)) #build in exact values for the check questions
#qnums.insert(6,str(len(questions)-1))
#qnums.insert(16,str(len(questions))) #assumes the check questions are the last two in questions
 
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

<p style="text-align:center"><font size="5"><br><br> <b>Hello! Thank you for participating in our research!</font></p></b>

<p style="text-align:left;margin-left:30px;margin-right:20px"><font size="4">
In this study, you will be reading a set of short passages. You will be asked to make simple judgments about each passage. There is no right or wrong answer, we are just interested in our opinion.
<br><br>
The data collected from this HIT will be used as part of a scientific research project. Your decision to complete this HIT is voluntary. We will not collect identifying information. Other than your responses, the only information we will have is the time at which you completed the survey and the amount of time you spent to complete it. Your data may be used in analyses presented at scientific meetings or published in scientific journals. Continuing with this study indicates that you are at least 18 years of age, and agree to complete this HIT voluntarily.
<br><br>
<b> If you accept these conditions and are ready to begin, please fill in your Subject ID (provided in your MTURK HIT) and click below. By continuing, you are providing consent to participate in this study. </b>
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
qnumlist=str(qnums)
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

