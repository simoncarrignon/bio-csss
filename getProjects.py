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

def check_name(name,project):
    fname=name.split("_")[0]
    #p=re.compile(".+"+fname.lower()+".+")
    #re.search(fname.lower,pproject.lower())
    return( re.search(r'\b'+fname.lower()+r'\b',project.lower()))

def write_proj(prjname,prjtxt,year,hid):
    #f = open("projects/"+str(year)+"/texts/"+prjname.encode("utf-8"), 'w')
    f = open("projects/"+str(year)+"/texts/"+str(hid)+"-"+prjname.encode("utf-8"), 'w')
    f.write(prjtxt.encode("utf-8"))
    f.close()

def get_all_history_ids(year,maxnum):
    baseurl="http://tuvalu.santafe.edu/events/workshops/index.php?title=Complex_Systems_Summer_School_"+str(year)+"-Projects_%26_Working_Groups&offset=20160622193918&limit="+str(maxnum)+"&action=history"
    response=get_html(baseurl)
    soup = BeautifulSoup(response.read(), 'html.parser') # convert the hml code in a bs4 object

    content=soup.body.find_all('a',attrs={'class':'mw-changeslist-date'}) #return the div with the content of the page
    allid=[]
    for link in content:
        m=re.search('oldid=([0-9]+)"',str(link))
        hid=m.group(1)
        allid.insert(0,int(hid))
    return(allid)

def get_all_projects(year,hid): 
    baseurl= "http://tuvalu.santafe.edu/events/workshops/index.php?title=Complex_Systems_Summer_School_"+str(year)+"-Projects_%26_Working_Groups" 
    #history="63307"
    if(hid):
        baseurl=baseurl+"&oldid="+str(hid)

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
    mypath="biographies/"+str(year)+"/people"
    listofpeople = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    prjname=""
    prjtxt=""
    mat=" "
    ###hedear of the matrix
    for name in listofpeople:
        mat=mat+","+name
    mat=mat+"\n"


    for elt in content.find_all(True,recursive=False): 
        if(elt.name == "h2"):
            if(curprj>0):
                mat=mat+'"'+prjname+'"'
                #fill the matrice if the firstname of the people is in the project description (pb with same firstname)
                for name in listofpeople:
                    if(check_name(name,prjtxt)):
                        mat=mat+","+str(1)
                        #print(name+" is in "+ prjname)
                    else:
                        mat=mat+","+str(0)
                mat=mat+"\n"
                write_proj(prjname,prjtxt,year,hid)
                prjtxt=""
            prjname=elt.get_text()
            prjname = prjname.replace("/", "-")
            listproj=listproj+","+'"'+prjname+'"'
            curprj=curprj+1
            print("projet "+str(curprj)+"/"+str(nbprj)+": "+prjname)
        else:
            if(curprj>0):
            #we follow saveing the text of the current project
                prjtxt=prjtxt+elt.get_text()+"\n"

    ###print the matrix filled on the fly:
    f = open("projects/"+str(year)+"/"+str(hid)+"participation_matrix-filled.csv", 'w')
    f.write(mat.encode("utf-8"))
    f.close()
    ####print the empty matrix
    #matrix=""
    #vir=","*nbprj
    #matrix=listproj+"\n"
    #for name in listofpeople:
    #    matrix=matrix+name+vir+"\n"
    #f = open("projects/"+str(year)+"/participation_matrix.csv", 'w')
    #f.write(matrix.encode("utf-8"))
    #f.close()
    ########

#main
def main():
    years=range(2011,2017)
    a=get_all_history_ids(2016,1500)
    cur=1
    for hid in a:
        print("revision "+str(hid)+": "+str(cur)+"/"+str(len(a)))
        get_all_projects(2016,hid)
        cur=cur+1
    print(a)
    #years=[2016]
    #for year in years:
    #    get_all_projects(year)
    #

main()
