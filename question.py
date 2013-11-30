#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
from qs import questions
from slist import subjects, keycodes

myform=cgi.FieldStorage()
cgitb.enable()
cursor = MySQLdb.connect(host="localhost",user="askerry",passwd="password",db="aesbehave").cursor()
print 'Content-type:text/html\n\n'


#cgitb.enable(display=0, logdir="/path/to/logdir")
print '''
<style type="text/css">
    body {
        font-family:verdana,arial,helvetica,sans-serif;
        font-size:100%;
    }
</style>
'''
#testing
theids=myform.keys()
subjid = myform['subjid'].value
match=0
if subjid in subjects: 
	subjindex=subjects.index(subjid)
	match=1
	keycode=keycodes[subjindex]
else: 
	match=0
if match==0:	
	print "<center><br><br> OOPS:<br>"
	print "The subject ID you have provided is incorrect. Please return to the previous page and re-enter the subject ID provided on your Mechanical Turk start page."
else:
        #print "your id is correct <br>"
        qnums=myform['qnums'].value
        qnums=qnums.split(",")
        #print "<p>these are the ids: %s </p>" %(theids)
        #print "<p>these are the qnums: %s </p>" %(qnums)
        qindex=myform['qindex'].value
        qindex=int(qindex)+1
        #print "<p>qindex: %s </p>" %(qindex)
        qnum=qnums[qindex-1]
        question=questions[int(qnum)-1]
        qindex=str(qindex)
        qnumlist=qnums[0]   
        count=0
        for q in qnums:
                count=count+1
                if count<len(qnums):
                        qnumlist=qnumlist+','+qnums[count]
        #print "<p>these are the new qnums: %s </p>" %(qnumlist)
        
        if int(qindex)==1:
       		#add the person to the database:  "insert" command for new rows
       		cursor.execute('insert into demographics_tbl (subjid) values (%s)',str(subjid))
       		formindex=cursor.execute("SELECT MAX(rownum) AS formindex FROM demographics_tbl")
       		formindex = cursor.fetchone()
       		#print "<p> %s </p>" % (formindex)
       		thisvar=str(formindex)
       		thisvar=thisvar[1:-3]
       		formindex=thisvar
       		#print "<p> type: %s </p>" % thisvar
        else:
       		lastQ=qnums[int(qindex)-2]
       		keycode=myform['keycode'].value
		formindex=myform['rownum'].value
       		lastresponse=myform['response'].value
       		qvar='q'+ lastQ
       		qvarw1=qvar+'otherword1'
       		qvarw2=qvar+'otherword2'
       		wlist=[qvarw1,qvarw2]
       		sql='update demographics_tbl set ' +qvar +' ="'+lastresponse+'" where rownum="'+formindex+'"'
       		cursor.execute(sql)
       		word=0
       		for x in ['otherword1', 'otherword2']:
               		word=word+1
               		try:
                       		it = myform[x].value
                       		newqvar=wlist[word-1]
                       		newsql='update demographics_tbl set '+newqvar+'="'+it+'" where rownum="'+formindex+'"'
                       		cursor.execute(newsql)
               		except: pass
        
        
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
        <style type="text/css" media="all">
	.radioLeft{
    		text-align:left;
		display:inline-block;	
	}
	label {
 		 margin-left: 10px;
		 margin-right: 15px;
	}
	</style>
	<script type="text/javascript">
        function validate(myform){
            if (!checkRadioArray(myform.response)) {alert('Please enter your rating!');return false;}
            return true;
        }
        function checkRadioArray(radioButtons){
            for (var i=0; i< radioButtons.length; i++) {
                if (radioButtons[i].checked) return true;
            }
            return false;
        }
        
        </script>
        </head>
        '''
        ####end of setup
        if int(qindex)<len(questions):
       		#print "main loop"
       		print "<center><b>Question %s/%s:</b><br><br>" % (qindex, len(questions))
       		print "<center>%s. <br><br>How does the character feel in this situation? <br> " % (question)
       		print '''
        	<div id="page_content" align="center">
        	<form name="myform" action="question.py" method="submit" onSubmit="return validate(myform)">
        	<div class="radioLeft" align="center">
                <br><input type="radio" name="response" value="good"><label for="good">good</label>
                <br><input type="radio" name="response" value="sad"><label for="sad">sad</label>
                <br><input type="radio" name="response" value="amused"><label for="amused">amused</label>
                <br><input type="radio" name="response" value="bad"><label for="bad">bad</label>
                <br><input type="radio" name="response" value="angry"><label for="angry">angry</label>
                <br><input type="radio" name="response" value="anxious"><label for="anxious">anxious</label>
                <br><input type="radio" name="response" value="scared"><label for="scared">scared</label>
                <br><input type="radio" name="response" value="lonely"><label for="lonely">lonely</label>
                <br><input type="radio" name="response" value="loving"><label for="loving">loving</label>
                </div>
                <div class="radioLeft" align="center">
                <br><input type="radio" name="response" value="good"><label for="good">good</label>
                <br><input type="radio" name="response" value="sad"><label for="sad">sad</label>
                <br><input type="radio" name="response" value="amused"><label for="amused">amused</label>
                <br><input type="radio" name="response" value="bad"><label for="bad">bad</label>
                <br><input type="radio" name="response" value="angry"><label for="angry">angry</label>
                <br><input type="radio" name="response" value="anxious"><label for="anxious">anxious</label>
                <br><input type="radio" name="response" value="scared"><label for="scared">scared</label>
                <br><input type="radio" name="response" value="lonely"><label for="lonely">lonely</label>
                <br><input type="radio" name="response" value="loving"><label for="loving">loving</label>
                </div>
                <div class="radioLeft" align="center">
                <br><input type="radio" name="response" value="good"><label for="good">good</label>
                <br><input type="radio" name="response" value="sad"><label for="sad">sad</label>
                <br><input type="radio" name="response" value="amused"><label for="amused">amused</label>
                <br><input type="radio" name="response" value="bad"><label for="bad">bad</label>
                <br><input type="radio" name="response" value="angry"><label for="angry">angry</label>
                <br><input type="radio" name="response" value="anxious"><label for="anxious">anxious</label>
                <br><input type="radio" name="response" value="scared"><label for="scared">scared</label>
                <br><input type="radio" name="response" value="lonely"><label for="lonely">lonely</label>
                <br><input type="radio" name="response" value="loving"><label for="loving">loving</label>
                </div>
                <div class="radioLeft" align="center">
                <br><input type="radio" name="response" value="good"><label for="good">good</label>
                <br><input type="radio" name="response" value="sad"><label for="sad">sad</label>
                <br><input type="radio" name="response" value="amused"><label for="amused">amused</label>
                <br><input type="radio" name="response" value="bad"><label for="bad">bad</label>
                <br><input type="radio" name="response" value="angry"><label for="angry">angry</label>
                <br><input type="radio" name="response" value="anxious"><label for="anxious">anxious</label>
                <br><input type="radio" name="response" value="scared"><label for="scared">scared</label>
                <br><input type="radio" name="response" value="lonely"><label for="lonely">lonely</label>
                <br><input type="radio" name="response" value="loving"><label for="loving">loving</label>
                </div>

		<br><br>
		<p> If you feel that the situation is better described by a word not <br> provided above, please list alternative words here (optional). </p>
        	<input type="text" name="otherword1" >
        	<br><input type="text" name="otherword2">
        	<br><br>
        	<input type="hidden" name="subjid" value="'''+subjid+'''">
        	<input type="hidden" name="keycode" value="'''+keycode+'''">
        	<input type="hidden" name="qindex" value="'''+qindex+'''">
        	<input type="hidden" name="qnums" value="'''+qnumlist+'''"> 
        	<input type="hidden" name="rownum" value="'''+formindex+'''"> 	
        	<input type="submit" value="Continue" /></center>
        	<br><br><br><br>
        	</form>
        	</div>
        	</body>
        	</html>
        	'''
        else:
	       	#print "final loop"
		print "Question %s/%s:<br>" % (qindex, len(questions))
       		print "%s. How does the target feel? " % (question)
       		print '''
        	<div id="page_content" align="center">
        	<form name="myform" action="demographics.py" method="submit" onSubmit="return validate(myform)">
        	<br><input type="radio" name="response" value="good">GOOD
        	<br><input type="radio" name="response" value="bad">BAD
        	<br>
        	<input type="text" name="otherword1" >
        	<br><input type="text" name="otherword2">
        	<br>
        	<p style="text-align:center">You have completed the primary task! We have a few quick follow up questions for you.</p>
        	<input type="hidden" name="subjid" value="'''+subjid+'''">
        	<input type="hidden" name="keycode" value="'''+keycode+'''">
        	<input type="hidden" name="qindex" value="'''+qindex+'''">
        	<input type="hidden" name="qnums" value="'''+qnumlist+'''">
        	<input type="hidden" name="rownum" value="'''+formindex+'''"> 
        	<input type="submit" value="Continue" /></center>
        	<br><br><br><br>
        	</form>
        	</div>
        	</body>
        	</html>
        '''
        
        
        
        #end

