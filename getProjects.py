#!/usr/bin/python
# -*- coding: utf-8 -*-
#Code used for the Complex System Summer School 2016
#contact: sc@elisya.org
#Todo : levenshtein on topic name & factorised the 2 .py files
#(create classes?)

from bs4 import BeautifulSoup
import urllib2
import csv
import re 
import os
import random

from os import listdir
from os.path import isfile, join


def get_list_people(year):
    mypath="biographies/"+str(year)+"/people"
    listofpeople = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    random.shuffle(listofpeople)
    return(listofpeople)

#Compute the levenshtein distance between two string 
#(reduce the cost of space?
#Give extra point for whole name match
def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings."""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
       distance_matrix[i][0] = i
    for j in range(second_length):
       distance_matrix[0][j]=j
    for i in xrange(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]

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

def get_id(name):
    k = open("/home/simon/key.csv")
    csvfile=csv.reader(k)
    #csvfile=csv.DictReader(k) (better if we had smallers header)
    headers=csvfile.next()
    names=[]
    procname=name.replace("_"," ").lower().strip() 
    dis=1000
    #key detection
    for row in csvfile:
        fn=row[0].strip()
        ln=row[1].strip()
        eid=int(row[2])
        cname=fn.lower().strip()+" "+ln.lower().strip()
        if(dis > levenshtein_distance(cname,procname) ):
            names.append([cname,eid])
            dis=levenshtein_distance(cname,procname)
    return(names.pop()) 


#Check if a given name is in the project text
def check_name(name,project):
    fname=name.split("_")[0]
    #p=re.compile(".+"+fname.lower()+".+")
    #re.search(fname.lower,pproject.lower())
    return( re.search(r'\b'+fname.lower()+r'\b',project.lower()))

#Write the text content of a project
def write_proj(prjname,prjtxt,year,hid):
    f = open("projects/"+str(year)+"/texts/"+str(hid)+"-"+prjname.encode("utf-8"), 'w')
    f.write(prjtxt.encode("utf-8"))
    f.close()

##Get the `maxnum` differents version of the project page  and return a list with the id and the date of the modification 
def get_all_history_ids(year,maxnum):
    baseurl="http://tuvalu.santafe.edu/events/workshops/index.php?title=Complex_Systems_Summer_School_"+str(year)+"-Projects_%26_Working_Groups&offset=20160725193918&limit="+str(maxnum)+"&action=history"
    response=get_html(baseurl)
    soup = BeautifulSoup(response.read(), 'html.parser') # convert the hml code in a bs4 object
    content=soup.body.find_all('a',attrs={'class':'mw-changeslist-date'}) #return the div with the content of the page

    allid=[]
    for link in content:
        m=re.search('oldid=([0-9]+)"',str(link))
        hid=m.group(1)
        newelt=[int(hid),link.get_text().replace(",","")]
        allid.insert(0,newelt)
    return(allid)

##Return all projects of one particular version of the project's page
def get_all_projects(year,hid,listofpeople): 
    baseurl= "http://tuvalu.santafe.edu/events/workshops/index.php?title=Complex_Systems_Summer_School_"+str(year)+"-Projects_%26_Working_Groups" 
    if(hid):
        baseurl=baseurl+"&oldid="+str(hid)
    print("trying to parse projects from: "+str(year))
    print(baseurl)
    
    #####
    #To get the url
    response=get_html(baseurl)
    soup = BeautifulSoup(response.read(), 'html.parser') # convert the hml code in a bs4 object
    content=soup.body.find('div',attrs={'id':'mw-content-text'}) #return the div with the content of the page


    curprj=0
    listproj=" "
    #if year == 2016: #work for some years.
    allproj=content.find_all('h2',recursive=False)
    nbprj=len(allproj)
    print(str(nbprj)+" projects found")

    prjname=""
    prjtxt=""
    mat=" "
    ###hedear of the matrix
    for name in listofpeople:
        mat=mat+","+str(get_id(name)[1])
    mat=mat+"\n"

    for elt in content.find_all(True,recursive=False): 
        if(elt.name == "h2"):
            if(curprj>0):
                mat=mat+'"'+prjname+'"'
                #fill the matrice if the firstname of the people is in the project description (pb with same firstname)
                for name in listofpeople:
                    if(check_name(name,prjtxt)):
                        mat=mat+","+str(1)
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

#main
def main():
    years=range(2011,2017)
    #years=[2016]
    for year in years:
        print(str(year))
        ##create necessary folders folder
        if not(os.path.isdir("projects")):
            os.mkdir("projects/")
        if not(os.path.isdir("projects/"+str(year))):
            os.mkdir("projects/"+str(year))
        if not(os.path.isdir("projects/"+str(year)+"/texts")):
            os.mkdir("projects/"+str(year)+"/texts")

        cur=1
        fileid = open("projects/"+str(year)+"/id.csv", 'w')
        fileid.write("id,time\n")
        listofpeople=get_list_people(year)
        allid=get_all_history_ids(year,1500)
        for i in range(1,len(allid),len(allid)/60):
            elt=allid[i]
            hid=elt[0]
            print("revision "+str(hid)+" ("+str(cur)+"/"+str(len(allid))+")")
            get_all_projects(year,hid,listofpeople)
            cur=cur+1
            fileid.write(str(elt[0])+","+str(elt[1])+"\n")
        fileid.close()

main()
