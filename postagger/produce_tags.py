import nltk
import json
import pysrt

from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import EnglishStemmer
snowball_stemmer = EnglishStemmer()

stop = stopwords.words('english')
text = """Nearly universally regarded as an improvement over porter, and for good reason. Porter himself in fact admits that Snowball is better than his original algorithm. Slightly faster computation time than snowball, with a fairly large community around it. 
Lancaster: Very aggressive stemming algorithm, sometimes to a fault. With porter and snowball, the stemmed representations are usually fairly intuitive to a reader, not so with Lancaster, as many shorter words will become totally obfuscated. The fastest algorithm here, and will reduced your working set of words hugely, but if you want more distinction, not the tool you would want."""
text = text.strip()		
text = nltk.word_tokenize(text)
tags = nltk.pos_tag(text)
print tags

our_tags = { "NN": wn.NOUN, "JJ":wn.ADJ, "VB":wn.VERB, "RB":wn.ADV }   
for j in tags:
  base_pos = j[1][:2]
  if((j[0] not in stop) and (base_pos in our_tags.keys())):
     wn_pos = our_tags[base_pos]
     stem=wnl.lemmatize(j[0], wn_pos)
     print "%s -> %s, %s" % (j,stem, snowball_stemmer.stem(j[0]))

