import matplotlib.pyplot as plt
from textblob import TextBlob
from senti import *

from flask import Flask,redirect, url_for , request,render_template
app = Flask(__name__)
   #starts ngrok when the app is run
@app.route('/')
def fu():
    return render_template("page.html")
@app.route('/tweet', methods =["GET", "POST"]) 
def gfg(): 
    if request.method == "POST": 
       # getting input with name = fname in HTML form 
       topic = request.form.get("topic") 
       # getting input with name = lname in HTML form  
       num = request.form.get("num")
       num=int(num) 
       a=Out()
       a.output(topic,int(num)) 
       pos=a.postweet
       neg=a.negtweet
       neu=a.neutweet
       p=[]
       n=[]
       ne=[]
       topic=topic.upper()
       
       pos=round(pos,2)
       neg=round(neg,2)
       neu=round(neu,2)
       
       
       for i in a.ptweets:
         p.append(i['text'])
         
       for i in a.ntweets:
         n.append(i['text'])
             
       for i in a.neutralt:
         ne.append(i['text'])
       
       return render_template("try2.html",pos=pos,neg=neg,neu=neu,p=p[:num],n=n[:num],ne=ne[:num],topic=topic)
    return render_template("test.html")



@app.route('/text', methods =["GET", "POST"]) 
def sfg():
    if request.method == "POST": 
       # getting input with name = fname in HTML form 
       text = request.form.get("t")
      
       blob=TextBlob(str(text))
       if(blob.sentiment[0]>0):
         res=0
       elif(blob.sentiment[0]<0):
         res=1
       else:
         res=2

       
       return render_template("sest.html",res=res,text=text)
    return render_template("sest.html",res=3)

if __name__ == '__main__':
  app.run()
