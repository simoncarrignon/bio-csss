#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import csv
import re 



baseurl = "http://tuvalu.santafe.edu/events/workshops/index.php/Complex_Systems_Summer_School_2016-Participants" 

basewiki= "http://tuvalu.santafe.edu/"
#####
url = baseurl
request = urllib2.Request(url)
request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
request.add_header('Content-Type','application/json')
response = urllib2.urlopen(request)
#To get the url


soup = BeautifulSoup(response.read(), 'html.parser') # beautifulsoup is the htmlparser used to dig in the html page.

alls=soup.body.find('div',attrs={'id':'mw-content-text'})

allp=alls.find_all('p')

table=allp[2] #There is probably a more robust way to get the name..

allstud=table.find_all('a',href=True)

for student in allstud: 
    print(student['href'])
    urlstud=basewiki+student['href']
    requeststud = urllib2.Request(urlstud)
    requeststud.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    requeststud.add_header('Content-Type','application/json')
    repstud = urllib2.urlopen(requeststud)
    
    studsoup = BeautifulSoup(repstud.read(), 'html.parser') 
    studinfo=studsoup.body.find('div',attrs={'id':'mw-content-text'})
    allpstud=studinfo.find_all('p')
    text=""
    for allpstud in allpstud:
        text= text+"\n" + allpstud.get_text()
    studname=urlstud.split('/')
    print(text.encode("utf-8"))
    print(studname)
    name=studname[len(studname)-1]
    print(name)
    f = open("people/"+name.encode("utf-8"), 'w')
    f.write(text.encode("utf-8"))
    f.close()
