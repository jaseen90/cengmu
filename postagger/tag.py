import nltk
import json
import pysrt
from nltk.tag.stanford import POSTagger
english_postagger = POSTagger('models/english-bidirectional-distsim.tagger', 'stanford-postagger.jar')
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
from nltk.tokenize import RegexpTokenizer
toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
from nltk.corpus import stopwords
stop = stopwords.words('english')
subs = pysrt.open('deneme.srt')
ignore = -1
j=0
myObj=[]
tok=[]
f = open('kelimeler', 'wr')
for (i,sub) in enumerate(subs):
   if ignore == i:
     ignore = -1
     continue
   text = sub.text.strip()
   if not text[-1] in ".!?":
      text += " "+subs[i+1].text
      ignore = i+1
   #print english_postagger.tag(text.split())[0][1]
   for j in english_postagger.tag(text.split()):
      #print i
     #print j[0]
     if ((j[0] not in stop) and (j[1] == "NN" or j[1] == "JJ" or j[1] == "VB")):
         start=str(sub.start)	
	 end=str(sub.end)
	 #tok=append.toker.tokenize(j[0])    
	 stem=wnl.lemmatize(j[0])
	 print wnl.lemmatize(stem)
         myObj.append([stem, {'baslamaSaati': (start)},{'bitisSaati':(end)},{'oge':(j[1])}])
   if (i==10): break
   
a = str(json.dumps(myObj))        
f.write(a)
