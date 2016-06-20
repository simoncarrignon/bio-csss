#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import csv
import re 
import os

def get_html(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    request.add_header('Content-Type','application/json')
    response = urllib2.urlopen(request)
    return(response)
def test_edit(name):
    p=re.compile(".+edit.+")
    m=p.match(name)
    return(m)

def get_all_participant(year): 
    baseurl = "http://tuvalu.santafe.edu/events/workshops/index.php/Complex_Systems_Summer_School_"+str(year)+"-Participants" 
    print("trying to get all students from: "+str(year))
    print(baseurl)
    
    basewiki= "http://tuvalu.santafe.edu/"
    #####
    #To get the url
    response=get_html(baseurl)
    soup = BeautifulSoup(response.read(), 'html.parser') # beautifulsoup is the htmlparser used to dig in the html page.
    
    content=soup.body.find('div',attrs={'id':'mw-content-text'})

    #alllink=list(content.descendants)[5:len(list(content.descendants))]
    
    alllink=content.find_all('a')
    alllink=alllink[19:75] #the other link are not participant

    print(str(year))
    if not(os.path.isdir(str(year))):
        os.mkdir(str(year))
    if not(os.path.isdir(str(year)+"/people")):
        os.mkdir(str(year)+"/people")

    for student in alllink: 
        urlstud=basewiki+student['href']
        studname=urlstud.split('/')
        studname=studname[len(studname)-1]
        print("parsing student: "+studname)
        text=""
        if test_edit(urlstud):
            print("student "+studname+" without bio")
            text="no bio written"
        else:        
            repstud = get_html(urlstud) 
            studsoup = BeautifulSoup(repstud.read(), 'html.parser') 
            studinfo=studsoup.body.find('div',attrs={'id':'mw-content-text'})
            allpstud=studinfo.find_all('p')
            for allpstud in allpstud:
                text= text+"\n" + allpstud.get_text()
            print(text.encode("utf-8"))

        f = open(str(year)+"/people/"+studname.encode("utf-8"), 'w')
        f.write(text.encode("utf-8"))
        f.close()

get_all_participant(2011)
