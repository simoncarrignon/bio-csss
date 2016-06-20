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
    p=re.compile(".*edit.*")
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
    
    alls=soup.body.find('div',attrs={'id':'mw-content-text'})
    
    allp=alls.find_all('p')
    
    table=allp[2] #There is probably a more robust way to get the name..
    
    allstud=table.find_all('a',href=True)
    print(str(year))
    if not(os.path.isdir(str(year))):
        os.mkdir(str(year))
    if not(os.path.isdir(str(year)+"/people")):
        os.mkdir(str(year)+"/people")

    for student in allstud: 
        urlstud=basewiki+student['href']
        studname=urlstud.split('/')
        studname=studname[len(studname)-1]
        print("parsing student: "+studname)
        text=""
        if test_edit(urlstud):
            print("student "+studname+" without bio")
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

#baseurl = "http://tuvalu.santafe.edu/events/workshops/index.php/Complex_Systems_Summer_School_2016-Participants" 


def main():
    years=range(2011,2017)
    for year in years:
        get_all_participant(year)
       # baseurl= "http://tuvalu.santafe.edu/events/workshops/index.php?title=Complex_Systems_Summer_School_"+y+"-Projects_%26_Working_Groups"
       # #basewiki= "http://tuvalu.santafe.edu/"
       # #####
       # url = baseurl
       # request = urllib2.Request(url)
       # request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
       # request.add_header('Content-Type','application/json')
       # response = urllib2.urlopen(request)
       # #To get the url
       # 
       # 
       # soup = BeautifulSoup(response.read(), 'html.parser') # beautifulsoup is the htmlparser used to dig in the html page.
       # 
       # alluser=soup.body.find_all('span',attrs={'class':'history-user'})
       # 
       # 
       # for user in alluser: 
       #     print(user.get_text())
            #urlstud=basewiki+student['href']
            #requeststud = urllib2.Request(urlstud)
            #requeststud.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
            #requeststud.add_header('Content-Type','application/json')
            #repstud = urllib2.urlopen(requeststud)
            #
            #studsoup = BeautifulSoup(repstud.read(), 'html.parser') 
            #studinfo=studsoup.body.find('div',attrs={'id':'mw-content-text'})
            #allpstud=studinfo.find_all('p')
            #text=""
            #for allpstud in allpstud:
            #    text= text+"\n" + allpstud.get_text()
            #studname=urlstud.split('/')
            #print(text.encode("utf-8"))
            #print(studname)
            #name=studname[len(studname)-1]
            #print(name)
            #f = open("people/"+name.encode("utf-8"), 'w')
            #f.write(text.encode("utf-8"))
            #f.close()

main()
