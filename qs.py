import csv

def getconfiguration(configfile):
    with open(configfile, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for subjnum, row in enumerate(reader):
            if subjnum==0:
                colnames=row
                reader = csv.reader(csvfile)
                rowdata=list(reader) 
                coldata=zip(*rowdata) #handytranspose
                emolistindex=colnames.index('emotionlist')
                nameindex=colnames.index('names')
                names=coldata[nameindex]
                emolist=coldata[emolistindex]
                emolist=[emo for emo in emolist if emo !='']
                names=[name for name in names if name !='']
    return emolist, names

def getquestions(stimfile):
    questions=[]
    emoanswers=[]
    with open(stimfile, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for subjnum, row in enumerate(reader):
            if subjnum==0:
                colnames=row
                print 'varnames in csv: '+str(colnames)
                questionindex=colnames.index('cause')
                emoanswerindex=colnames.index('emotion')
                incindex=colnames.index('keeper')
            else:
                subjdata=row
                if int(subjdata[incindex]):
                    quest=subjdata[questionindex]
                    #print quest
                    quest=quest.replace("!!!","\'" )
                    questions.append(quest)
                    emoanswers.append(subjdata[emoanswerindex])
    return questions, emoanswers
                    
#stimfile='/Users/amyskerry/Documents/projects/turk/NDE/NDE_stims.csv'
#configfile='/Users/amyskerry/Documents/projects/turk/NDE/config.csv'
stimfile='NDE_stims.csv'
configfile='config.csv'
[emolist, names]=getconfiguration(configfile)
[questions, emoanswers]=getquestions(stimfile)
