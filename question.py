#!/usr/bin/python

import cgitb, cgi, MySQLdb, ast
#import cgitb, cgi, ast
import cPickle as p
from random import randint, shuffle
from ast import literal_eval
from qs import questions, names, emolist
from slist import subjects, keycodes
import math

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
        qnums=eval(myform['qnums'].value)
	qnums=map(lambda x:int(x), qnums)
	#qnums=qnums.split(",")
        #print "<p>these are the ids: %s </p>" %(theids)
        #print "<p>these are the qnums: %s </p>" %(qnums)
        qindex=myform['qindex'].value
        qindex=int(qindex)+1
        #print "<p>qindex: %s </p>" %(qindex)
        qnum=qnums[qindex-1]
        question=questions[qnum-1]
        qname=names[qnum-1]
        question=question.replace('NAMEVAR', qname)
        qindex=str(qindex)
        #qnumlist=qnums[0]   
        #count=0
        #for q in qnums:
        #        count=count+1
        #        if count<len(qnums):
        #                qnumlist=qnumlist+','+qnums[count]
        #print "<p>these are the new qnums: %s </p>" %(qnumlist)
        qnumlist=str(qnums)
        if int(qindex)==1:
       		#add the person to the database:  "insert" command for new rows
       		cursor.execute('insert into NDE_table (subjid) values (%s)',str(subjid))
       		formindex=cursor.execute("SELECT MAX(rownum) AS formindex FROM NDE_table")
       		formindex = cursor.fetchone()
       		#print "<p> %s </p>" % (formindex)
       		thisvar=str(formindex)
       		thisvar=thisvar[1:-3]
       		formindex=thisvar
       		#print "<p> type: %s </p>" % thisvar
        else:
       		lastQ=str(qnums[int(qindex)-2])
       		keycode=myform['keycode'].value
		formindex=myform['rownum'].value
       		lastresponse=myform['response'].value
       		qvar='q'+ lastQ
       		qvarw1=qvar+'otherword1'
       		qvarw2=qvar+'otherword2'
       		wlist=[qvarw1,qvarw2]
       		sql='update NDE_table set ' +qvar +' ="'+lastresponse+'" where rownum="'+formindex+'"'
       		cursor.execute(sql)
       		word=0
       		for x in ['otherword1', 'otherword2']:
               		word=word+1
               		try:
                       		it = myform[x].value
                       		newqvar=wlist[word-1]
                       		newsql='update NDE_table set '+newqvar+'="'+it+'" where rownum="'+formindex+'"'
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
    		text-align: center;
		display:inline-block;	
	}
	label { 		 
		 margin-left: 15px;
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
	nextthing='question.py'
        if int(qindex)<len(questions):
		nextthing='question.py'
	else:
		nextthing='demographics.py'       	
	#print "main loop"
       	print "<center><b>Question %s/%s:</b><br><br>" % (qindex, len(questions))
       	print "<center>%s. <br><br>How does the character feel in this situation? <br> " % (question)
       	print '''
        <div id="page_content" align="center">
        <form name="myform" action="%s" method="submit" onSubmit="return validate(myform)">
        <div class="radioLeft" align="center">
        '''%(nextthing)
	def make_checkarray(emotionlist):
		numemos=len(emotionlist)
		#numcols=math.floor(math.sqrt(numemos))
		if numemos<4:
			numcols=numemos
		else:
			numcols=math.floor(math.sqrt(len(emolist)))
		buckets=[[] for i in range(0,numcols)]
		for n, emo in enumerate(emotionlist):
			col=int(n%numcols)
			emostring='<br><input type="radio" name="response" value="%s"><label for="%s">%s</label>' % (emo,emo,emo)
			buckets[col].append(emostring)
		mainprintout=[]
		for c in buckets:
			print '<div class="radioLeft" align="center">'
			for e in c:
				print e
			print "</div>"
	make_checkarray(emolist)
	print '''
	<br><br>
	<p> If you feel that the situation is better described by another <br> word, please list alternative words here (optional). </p>
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
        
        #end

