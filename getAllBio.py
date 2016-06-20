#!/usr/bin/python
# -*- coding: utf-8 -*-
#Code used for the Complex System Summer School 2016
#contact: sc@elisya.org

from bs4 import BeautifulSoup
import urllib2
import csv
import re 
import os



#get_html return the html code of a given page with adresse: url 
def get_html(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    request.add_header('Content-Type','application/json')
    response = urllib2.urlopen(request)
    return(response)

#this fuction return something if the user page has not be filled (meaning that the bio is empty)
#TODO: should return the name instead of the match
def test_edit(name):
    p=re.compile(".+edit.+")
    m=p.match(name)
    return(m)

#this function go to the page of a given student with a relative url "student" and 
#Write the biography of this student in the folder of the given year 
def write_bio(student,year):
    basewiki= "http://tuvalu.santafe.edu/"
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

#Main function: look to all participants and write there biography
def get_all_participants(year): 
    baseurl = "http://tuvalu.santafe.edu/events/workshops/index.php/Complex_Systems_Summer_School_"+str(year)+"-Participants" 
    print("trying to get all students from: "+str(year))
    print(baseurl)
    
    #####
    #To get the url
    response=get_html(baseurl)
    soup = BeautifulSoup(response.read(), 'html.parser') # convert the hml code in a bs4 object
    
    content=soup.body.find('div',attrs={'id':'mw-content-text'}) #return the div with the content of the page

    print(str(year))
    if not(os.path.isdir(str(year))):
        os.mkdir(str(year))
    if not(os.path.isdir(str(year)+"/people")):
        os.mkdir(str(year)+"/people")

    if year == 2011: #for 2011 we cannot use the "Participants" title as they didn't put such title
        alllink=content.find_all('a')
        alllink=alllink[19:75] #the other link are not participant
        for student in alllink: 
            write_bio(student,year)

    else:
        isstud=False
        for elt in content.find_all(True,recursive=False): 
            #print(elt)
            #print("------------------------------")
            if isstud: #we parse only if participants title was already found
                allstudent=elt.find_all('a')
                if len(allstudent) == 1 : #this case is use for the 2012 summer school
                    write_bio(allstudent[0],year)
                else: #all case from 2013 to 2016
                    for student in allstudent:
                        write_bio(student,year)
                        isstud=False

            span=elt.find_all('span',attrs={'id':'Participants'}) #if we reach the "Participants" title, we can start to parse
            if span:
                print(span) 
                isstud=True
                print("------------------------------------------------------------")
                print("Start parsing student:")


#main
def main():
    years=range(2011,2017)
    for year in years:
        get_all_participants(year)
    
main()

