#!/usr/bin/python
# -*- coding: utf-8 -*-
#Code used for the Complex System Summer School 2016
#contact: sc@elisya.org

from bs4 import BeautifulSoup
import urllib2
import csv
import re 
import os

from os import listdir
from os.path import isfile, join


#get_html return the html code of a given page with adresse: url 
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

def write_proj(prjname,prjtxt,year):
    f = open(str(year)+"/texts/"+prjname.encode("utf-8"), 'w')
    f.write(prjtxt.encode("utf-8"))
    f.close()

def get_all_projects(year): 
    baseurl= "http://tuvalu.santafe.edu/events/workshops/index.php?title=Complex_Systems_Summer_School_"+str(year)+"-Projects_%26_Working_Groups" 
    history="&oldid=63307"
    isOld=False
    if isOld:
        baseurl=baseurl+history

    print("trying to parse projects from: "+str(year))
    print(baseurl)
    
    #####
    #To get the url
    response=get_html(baseurl)
    soup = BeautifulSoup(response.read(), 'html.parser') # convert the hml code in a bs4 object
    
    content=soup.body.find('div',attrs={'id':'mw-content-text'}) #return the div with the content of the page

    print(str(year))
    if not(os.path.isdir(str(year))):
        os.mkdir(str(year))
    if not(os.path.isdir(str(year)+"/texts")):
        os.mkdir(str(year)+"/texts")

    curprj=0
    listproj=" "
    #if year == 2016: #work for some years.
    allproj=content.find_all('h2',recursive=False)
    nbprj=len(allproj)
    print(str(nbprj)+" projects found")

    prjname=""
    prjtxt=""
    for elt in content.find_all(True,recursive=False): 
        if(elt.name == "h2"):
            if(curprj>0):
                write_proj(prjname,prjtxt,year)
                prjtxt=""
            prjname=elt.get_text()
            prjname = prjname.replace("/", "-")
            listproj=listproj+","+'"'+prjname+'"'
            curprj=curprj+1
            print("projet "+str(curprj)+"/"+str(nbprj)+": "+prjname)
        else:
            if(curprj>0):
                prjtxt=prjtxt+elt.get_text()+"\n"
    matrix=""
    vir=","*nbprj
    mypath="../biographies/"+str(year)+"/people"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    matrix=listproj+"\n"
    for name in onlyfiles:
        matrix=matrix+name+vir+"\n"
    f = open(str(year)+"/participation_matrix.csv", 'w')
    f.write(matrix.encode("utf-8"))
    f.close()
#main
def main():
    years=range(2011,2017)
    #years=[2016]
    for year in years:
        get_all_projects(year)
    
main()

