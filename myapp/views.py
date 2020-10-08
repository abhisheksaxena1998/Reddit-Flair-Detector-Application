#!/usr/bin/python
# -*- coding: utf-8 -*-
def warn(*args, **kwargs):
    pass

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import *


# Create your views here.

def automated_testing(request):
    import praw
    import re
    import json
    import requests


    if request.method == "POST":
        uploaded_file = request.FILES['upload_file']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        f = open("media/"+uploaded_file.name, "r")
        #print(f.read())
        storage=[]
        num=0
        dis=[]    
        for x in f:
            d={}
            x=x.replace('\n','')                    
            nm=x
            try:                 
                reddit = praw.Reddit(client_id='WBTxS7rybznf7Q', client_secret='vJUTUflXITBsQMxeviOfG8mCZoA', user_agent='projectreddit', username='Mysterious_abhE', password='Saxena0705')
                submission = reddit.submission(url=nm)
                submission.comments.replace_more(limit=0)
                tr=[]
                c=''
                for top_level_comment in submission.comments:        
                    c+=top_level_comment.body  
                tr=submission.title+nm+c
                processed_tweet = re.sub(r'\W', ' ', tr)
                processed_tweet = re.sub(r'http\S+', ' ', processed_tweet)
                processed_tweet=re.sub(r'www\S+', ' ', processed_tweet)
                processed_tweet=re.sub(r'co \S+', ' ', processed_tweet)
                processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)
                processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 
                processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
                processed_tweet = re.sub(r'^b\s+', ' ', processed_tweet)
                processed_tweet = re.sub(r'\d','',processed_tweet)
                processed_tweet = re.sub(r'\_',' ',processed_tweet)
                processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
                tr = processed_tweet.lower()   
                filename = 'SGD_model1002moddata.sav'
                loaded_model = joblib.load(filename)
                arg=loaded_model.predict(([tr]))
                #print (arg[0])
                d.update({"key":x})
                d.update({"value":arg[0]})
                dis.append(d)
            except:
                d.update({"key":x})
                d.update({"value":"Invalid URL"})
                dis.append(d)
                    

        #print (dis)        
        response = JsonResponse(dis,safe=False)
        return (response)





def upload(request):
    import requests

    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        f = open("media/"+uploaded_file.name, "r")
        #print(f.read())
        storage=[]
        num=0

        '''Content=f.read()
        CoList = Content.split("\n") 
 
        for i in CoList: 
            if i:
                num+=1
        print ("Size",num) '''        
        #working
        """for x in f:
            response=requests.get(f"http://reddit-realtime-analysis.herokuapp.com/api?query={x}")
            storage.append((response.text))
            num+=1
        print (num)
        print (storage)   
"""
            
    return render(request,'upload.html')

def APIresult(request):
        import requests
        import json
        import praw
        import re        
        import datetime
        import joblib
        uploaded_file = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        f = open("media/"+uploaded_file.name, "r") 
        dis=[]    
        for x in f:
            d={}
            x=x.replace('\n','')                    
            nm=x
            try:                 
                reddit = praw.Reddit(client_id='WBTxS7rybznf7Q', client_secret='vJUTUflXITBsQMxeviOfG8mCZoA', user_agent='projectreddit', username='Mysterious_abhE', password='Saxena0705')
                submission = reddit.submission(url=nm)
                submission.comments.replace_more(limit=0)
                tr=[]
                c=''
                for top_level_comment in submission.comments:        
                    c+=top_level_comment.body  
                tr=submission.title+nm+c
                processed_tweet = re.sub(r'\W', ' ', tr)
                processed_tweet = re.sub(r'http\S+', ' ', processed_tweet)
                processed_tweet=re.sub(r'www\S+', ' ', processed_tweet)
                processed_tweet=re.sub(r'co \S+', ' ', processed_tweet)
                processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)
                processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 
                processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
                processed_tweet = re.sub(r'^b\s+', ' ', processed_tweet)
                processed_tweet = re.sub(r'\d','',processed_tweet)
                processed_tweet = re.sub(r'\_',' ',processed_tweet)
                processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
                tr = processed_tweet.lower()   
                filename = 'SGD_model1002moddata.sav'
                loaded_model = joblib.load(filename)
                arg=loaded_model.predict(([tr]))
                print (arg[0])
                d.update({"key":x})
                d.update({"value":arg[0]})
                dis.append(d)
            except:
                d.update({"key":x})
                d.update({"value":"Invalid URL"})
                dis.append(d)
                    

        print (dis)        
        response = JsonResponse(dis,safe=False)
        return (response)

        #return render(request,'APIresult.html',{'storage':response})

def error_404_view(request, exception):
    return render(request,'404.html')

def index(request):
    try:
        return render(request, 'index.html')
    except:
        return render(request, '404.html')


def getuserfeedbackform(request):
    try:
        return render(request, 'userfeedbackform.html')
    except:
        return render(request, '404.html')

def dataanalysis(request):
    return render(request,'dataanalysis.html')

def saveuserfeedbackform(request):
    try:
        obj = UserFeedBack()
        obj.title = request.GET['usertitle']
        obj.description = request.GET['userdescription']
        obj.save()
        mydict = {'feedback': True}
        return render(request, 'userfeedbackform.html', context=mydict)
    except:
        return render(request, '404.html')

import warnings
warnings.warn = warn
import warnings
from lxml import html
from json import dump, loads
from requests import get
import json
from re import sub
from dateutil import parser as dateparser
from time import sleep
from django.http import HttpResponse
from django.shortcuts import render
import os
import pickle
import joblib #from sklearn.externals import joblib
import datetime


def result(request):

    text=request.GET['url']
    try:
        uq=text[43:45]+".txt"
        imgname=text[43:45]+".png"
        location="static/"+imgname
        loc="/static/"+imgname
        import praw
        import re
        nm=text  #"https://www.reddit.com/r/india/comments/fwcz7h/firozabad_police_factchecking_zee_news/"
        reddit = praw.Reddit(client_id='WBTxS7rybznf7Q', client_secret='vJUTUflXITBsQMxeviOfG8mCZoA', user_agent='projectreddit', username='Mysterious_abhE', password='Saxena0705')
        submission = reddit.submission(url=nm)
        #print (submission.comments[0])
        #print (submission.title)
        submission.comments.replace_more(limit=0)
        #co=[]
        tr=[]
        c=str()
        for top_level_comment in submission.comments:        
            c+=top_level_comment.body  


        tr=submission.title+" "+nm+" "+c
        tle=submission.title
        actual=submission.link_flair_css_class
        
    except:
        tr=text
        tle="Not present in Reddit"
        c="Not present in Reddit"
        actual="Not present in Reddit"
    processed_tweet = re.sub(r'\W', ' ', tr)


    # Remove all the special characters

    processed_tweet = re.sub(r'http\S+', ' ', processed_tweet)

    #processed_tweet = re.sub(r'https?:\/\/+', ' ', processed_tweet)

    #processed_tweet=re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ',processed_tweet)

    processed_tweet=re.sub(r'www\S+', ' ', processed_tweet)

    processed_tweet=re.sub(r'co \S+', ' ', processed_tweet)
    # remove all single characters
    processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)

    # Remove single characters from the start
    processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 

    # Substituting multiple spaces with single space
    processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)

    # Removing prefixed 'b'
    processed_tweet = re.sub(r'^b\s+', ' ', processed_tweet)

    processed_tweet = re.sub(r'\d','',processed_tweet)
    processed_tweet = re.sub(r'\_',' ',processed_tweet)

    processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)


    # Converting to Lowercase
    tr = processed_tweet.lower()
    
    '''import csv
    if actual is not "Not present in Reddit":
        with open ('static/trainable.csv','a',encoding="utf-8") as res:        
            writer=csv.writer(res)      
            s="{},{}\n".format(re.sub(r'\W', ' ', (tr)),re.sub(r'\W', '', str(actual)))
            res.write(s)    
            print ("Successfull data saved")''' 



    import datetime
    import joblib

    #filename = 'SGD_model0.02v2cleaned.sav'
    filename ='SGD_model1002moddata.sav'
    loaded_model = joblib.load(filename)

    arg=loaded_model.predict(([tr]))
    print (arg[0])
    

    link=text
    flair=arg[0]
    obj = Url()
    obj.result = arg[0]
    obj.link = text
    obj.flair = arg[0]
    obj.title=tle
    tags = [result,link,flair]
    tags = list(filter(lambda x: x!="Not Found",tags))
    tags.append(text)
    obj.save()

    import csv
    with open ('static/dataset.csv','a') as res:        
        writer=csv.writer(res)           
        s="{},{},{},{}\n".format(re.sub(r'\W', '', text),re.sub(r'\W', ' ', tle),arg[0],str(datetime.datetime.now()))
        res.write(s)     

            
    return render(request,'result.html',{'result':'Real-time analysis successfull','f2':text,'mal': arg[0],'actual':actual,'title':tle,'Comments':c})



    '''  
    except:
        return render(request,'404.html')'''


def api(request):    
        text=request.GET['query']
        try:
            import praw
            nm=text  #"https://www.reddit.com/r/india/comments/fwcz7h/firozabad_police_factchecking_zee_news/"
            reddit = praw.Reddit(client_id='WBTxS7rybznf7Q', client_secret='vJUTUflXITBsQMxeviOfG8mCZoA', user_agent='projectreddit', username='Mysterious_abhE', password='Saxena0705')
            submission = reddit.submission(url=nm)
            #print (submission.comments[0])
            #print (submission.title)
            submission.comments.replace_more(limit=0)
            #co=[]
            tr=[]
            c=''
            for top_level_comment in submission.comments:        
                c+=top_level_comment.body  


            tr=submission.title+nm+c
            import datetime
            import joblib

            filename = 'SGD_model1002moddata.sav'

            loaded_model = joblib.load(filename)

            arg=loaded_model.predict(([tr]))
            print (arg[0])


            mydict = {
                "query" : text,
                "flair" : arg[0],
                "datetime" : str(datetime.datetime.now())
            }
            response = JsonResponse(mydict)
            return response

                

        except:
            mydict = {
                "query" : text,
                "flair" : "Invalid Url",
                "datetime" : str(datetime.datetime.now())
            }
            response = JsonResponse(mydict)
            return response
            
def themes(request):
    #return HttpResponse("about")
    try:
        return render(request, 'themes.html')
    except:
        return render(request, 'themes.html')
        

def about(request):
    #return HttpResponse("about")
    try:
        return render(request, 'about.html')
    except:
        return render(request, 'about.html')
    
def geturlhistory(request):
    mydict = {
        "urls" : Url.objects.all().order_by('-created_at')
    }
    return render(request,'list.html',context=mydict)
    '''except:
        return render(request,'404.html')
'''
def discuss(request):
    try:
        mydict = {
            "users" : UserFeedBack.objects.all()
        }
        return render(request,'discuss.html',context=mydict)
    except:
        return render(request,'404.html')

def search(request):
    try:
        query = request.GET['search']
        query = str(query).lower()
        mydict = {
            "urls" : Url.objects.all().filter(Q(link__contains=query) | Q(result__contains=query) | Q(created_at__contains=query) |
            Q(flair__contains=query) | Q(title__contains=query) 
            ).order_by('-created_at')
        }
        return render(request,'list.html',context=mydict)
    except:
        return render(request,'404.html')
        
    
def replyform(request,replyid):
    try:
        obj = UserFeedBack.objects.get(userid=replyid)
        mydict = {
        "replyid" : obj.userid,
        "title" : obj.title,
        "description" : obj.description
        }
        return render(request,'reply.html',context=mydict)
    except:
        return render(request,'404.html')

def savereply(request):
    try:
        print("debug start")
        replyid = request.GET['replyid']
        print(replyid)
        obj = UserFeedBack.objects.get(userid=replyid)
        obj.replied = True
        obj.reply = request.GET['userreply']
        obj.save()
        mydict = {
            "reply" : True,
            "users" : UserFeedBack.objects.all()
        }
        print("debug end")
        return render(request,'discuss.html',context=mydict)

    except:
        return render(request,'404.html')

def searchdiscuss(request):
    try:
        query = request.GET['search']
        query = str(query).lower()
        mydict = {
            "users" : UserFeedBack.objects.all().filter(Q(title__contains=query) | Q(description__contains=query) | Q(created_at__contains=query)
            |  Q(replied__contains=query) | Q(reply__contains=query)
            )
        }
        return render(request,'discuss.html',context=mydict)
    except:
        return render(request,'404.html')

def getdataset(request):
    try:
        return render(request,'getdataset.html')
    except:
        return render(request,'404.html')
			
