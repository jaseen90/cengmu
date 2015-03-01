import nltk
import json
import pysrt

from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

from nltk.corpus import stopwords
stop = stopwords.words('english')
subs = pysrt.open('deneme2.srt', encoding='iso-8859-1')
ignore = -1
j=0
tags=[]
tok=[]
end = 0
f = open('yenii', 'wr')

ignoreList = []
new_sub = None
new_subs = []
for (i,sub) in enumerate(subs):
  #print "Processing : %s i:%d il:%s" % (sub.text, i, ignoreList)	
  text = sub.text.strip() 
  if ignoreList == []:
      new_sub = { 'start': sub.start, 'text': "" }
  if text[-1] not in ".!?":
    ignoreList.append(i+1)
    new_sub['text'] += " " + text
    new_sub["end"] = sub.end  
  else:
    new_sub["end"] = sub.end
    new_sub["text"] += " " + text
    new_subs.append(new_sub)
  if i in ignoreList:
    ignoreList.pop(0)

frame = 5 * 1000   # 5 seconds before and after
for (i,sub) in enumerate(new_subs):
  # start time of scene
  try:
      j = i - 1
      start1 = sub['start']
      if j < 0:
         start = start1 - pysrt.SubRipTime(milliseconds=frame/2)
      else:          
          start2 = new_subs[j]['start']
          if start1 - start2 > frame:
             start = start1 - pysrt.SubRipTime(milliseconds=frame/2)
          else:
            while (j >= 0 and start1 - start2 < frame):
              start = start2
              j -= 1
              start2 = new_subs[j]['start']

      # end time of scene
      j = i + 1
      end1 = sub['end']
      if j == len(new_subs):
          end = end1 + pysrt.SubRipTime(milliseconds=frame/2)
      else:          
          end2 = new_subs[j]['end']
          if end2 - end1 > frame:
            end = end1 + pysrt.SubRipTime(milliseconds=frame/2)
          else:
            while (j < len(new_subs) and end2 -end1 < frame):
              end = end2
              j += 1
              end2 = new_subs[j]['end']  
  except IndexError as e:
      print "j=%s i=%d, sub=%s" % (j, i, sub)
      raise e  
  scene = { 'sentence': sub['text'], 'start': start, 'end': end }
  #print "%s time: %s" % (sub['text'],str(end - start))
  
  text = sub['text'].strip()		
  text = nltk.word_tokenize(text)
  tags = nltk.pos_tag(text)
  #print tags

  for j in tags:
    if((j[0] not in stop) and (j[1] == "NN" or j[1] == "JJ" or j[1] == "VB")):
	stem=wnl.lemmatize(j[0])
        scene = { 'sentence': sub['text'], 'start': start, 'end': end, 'word':stem }
        print "scene: %s\n" % (scene)
        f.write(str(scene)+ "\n")

"""
for (i,sub) in enumerate(subs):
   if ignore == i:
     ignore = -1
     continue
   text = sub.text.strip()
   end=str(subs[i].end)
   if not text[-1] in ".!?":
      text += " "+subs[i+1].text
      ignore = i+1
      end = str(subs[i+1].end)
   #print english_postagger.tag(text.split())[0][1]
   for j in english_postagger.tag(text.split()):
      #print i
     #print j[0]
     if ((j[0] not in stop) and (j[1] == "NN" or j[1] == "JJ" or j[1] == "VB")):
         l=-1
         start=str(sub.start)	
	 #end=str(sub.end)
	 tok=toker.tokenize(j[0])    
	# print tok
	 stem=wnl.lemmatize(tok[0])
	# print wnl.lemmatize(stem)
        # myObj.append([stem, {'baslamaSaati': (start)},{'bitisSaati':(end)},{'oge':(j[1])}])
	 for k in range (0,len(myObj)):
	    if myObj[k][0]==stem:			
		print stem
		print myObj[k][0]
		myObj[k][1].append([{'baslamaSaati': (start)},{'bitisSaati':(end)},{'oge':(j[1])},{'cumle':(text) ])				
		l=k
		break	
	 print l
	 if l==-1:
	        myObj.append([stem, [[{'baslamaSaati': (start)},{'bitisSaati':(end)},{'oge':(j[1])},{'cumle':(text)}]]])
   if (i==10): break
a = str(json.dumps(myObj))        
f.write(a)
"""
