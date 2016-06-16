#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import csv
import re 



baseurl = "http://tuvalu.santafe.edu/events/workshops/index.php/Complex_Systems_Summer_School_2016-Participants" #the base url : we look only the tab "characteristic" of each amphora web page

basewiki= "http://tuvalu.santafe.edu/"
#####
url = baseurl
request = urllib2.Request(url)
request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
request.add_header('Content-Type','application/json')
response = urllib2.urlopen(request)
#To get the url


soup = BeautifulSoup(response.read(), 'html.parser') # beautifulsoup is the htmlparser used to dig in the html page.
#primarylist=soup.body.find('ul',attrs={'class':'primary_list'},href=True)

alls=soup.body.find('div',attrs={'id':'mw-content-text'})

allp=alls.find_all('p')

table=allp[2] #There is probably a more robust way to get the name..

allstud=table.find_all('a',href=True)

for student in allstud: #manually looking at various ID I decide that 380 was the higher id they give
    print(student['href'])
    urlstud=basewiki+student['href']
    requeststud = urllib2.Request(urlstud)
    requeststud.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    requeststud.add_header('Content-Type','application/json')
    repstud = urllib2.urlopen(requeststud)
    
    studsoup = BeautifulSoup(repstud.read(), 'html.parser') # beautifulstudsoup is the htmlparser used to dig in the html page.
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
#
#    lyrics=songsoup.body.find('div',attrs={'class':'lyrics'})
#    songtitle=songsoup.body.find('span',attrs={'class':'text_title'})
#
#    tow=lyrics.get_text().encode("utf-8")
#    all_lyrics=lyrics.find_all('p')
#
#    f = open(title.encode("utf-8"), 'w')
#    f.write(tow)
#    f.close()
#
#    #a_name contains amphora name, it appears only once for each page and if the id is not associated with an amphora a_name doesn't exist
#    if(a_name):
#        elt=[str(i)]
#        elt.append('"'+a_name.string.encode("utf-8").strip()+'"')
#        alltd=soup.body.find_all('td', attrs={'class':'dets'})
#
#        #Basically, the "characteristics" page is a 'tbody' element, where every "td" is a different characteristic of the amphora
#
#        if(len(alltd) == 0): #sometimes, even if a_name existe, beautifulsoup cannot find the "td" inside the 'tbody': it's because some html tag are badly close when some amphora information (such as drawings) are missing
#           print("problem with: "+a_name.string+", id: "+str(i)) #this print the problematic amphora, to comment if you need a clean CSV
#        for t in  alltd: 
#            #there are different formats of 'td' : 
#            #       all 'td' have a title (found in a 'span' with class "bbi") which seems to be the characteristic's name. 
#            #       a) the characteristics : "rim type" "shoulder type" "handles in profle " "handles in sections" "neck type" "body type" and "base type" have : a title , a link and a description. The link correspond to a characteristic type but it could be missing, which means that this caracteristics is unsure or "to be advised" for this amphora, and sometimes the description is missing. 
#            #       b) the characteristics : "height" "width" and "rim dimater" have only a description which could be sometime only something like "12cm" sometimes "10cm-20cm" and sometimes "unsure"
#            #       c) the characteristic : "capacity" has only a description like the previous but is this time something like "20 - 40 litres" or  "unsure" 
#            #       d) the characteristic : "Fabric" is sometimes present, sometimes not, and his made with a description which should be a link to the fabric page (but often link to nowhere)
#            if(len(t.contents) == 4): #case c)
#                elt.append('"'+t.contents[3].string.encode("utf-8").strip()+'"')
#            if(len(t.contents) == 2):
#                elt.append("")
#                elt.append("")
#            if(len(t.contents) == 6):
#                if(t.contents[0].string.encode("utf-8").strip() == "Fabric"):  #case d)
#                    elt.append('"'+t.contents[3].string.encode("utf-8").strip()+'"')
#                else:
#                    elt.append('"'+t.contents[2].string.encode("utf-8").strip()+'"') #case a)
#                    elt.append('"'+t.contents[5].string.encode("utf-8").strip()+'"')
#            if(len(t.contents) == 3): #case b)
#                v=t.contents[2].string.encode("utf-8").strip()
#                n=[re.search("[\d.]+",i).group() for i in v.split("-")] #this is to remove the "cm" and if there is to value like 10cm - 20cm, to split them
#                if(len(n) == 1):
#                    elt.extend([n[0],n[0]])
#                else:
#                    elt.extend(n)
#        if(len(elt)>2):print(','.join(elt))
#
