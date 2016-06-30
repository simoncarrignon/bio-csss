import csv
import re 
from os import listdir
from os.path import isfile, join

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


def fix_null_byte(filename):
    fi = open(filename, 'rb')
    data = fi.read()
    fi.close()
    fo = open(filename, 'wb')
    fo.write(data.replace('\x00', ''))
    fo.close()

def get_all_files(mypath):
    listoffile = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return(listoffile)


allcsv=get_all_files("CSV/")
k = open("/home/simon/key.csv")
keyfile=csv.reader(k)
headers=keyfile.next()
allkey=list(keyfile)

anon=dict() #Anon will be the dictionnary with the match between name and ID

for f in allcsv:
    print(f)
    #the following is to fix some problem with the monkeysurvey file
    try:
        ff = open("CSV/"+f,'rb')
        csvfile=csv.reader(ff)
    except :
        print("fixing: "+f)
        fix_null_byte("CSV/"+f)

    #skyp and record first lines
    header=csvfile.next()
    names=csvfile.next()

    #The second line contains all the names so we have to loop on it
    for i in names:
        fname=i.split("-")[0]
        if(fname in anon):
            a=1 #if the key exist already no need to add it
        else:
            match_names=list()
            if(fname):
               # print("csv:"+fname)
                fnamel=fname.lower()
                dis=1000
                for row in allkey:
                    #print(row)
                    fn=row[0].strip()
                    ln=row[1].strip()
                    eid=int(row[2])
                    cname=fn.lower().strip()+" "+ln.lower().strip()
                    if(dis > levenshtein_distance(cname,fnamel) ):
                        match_names.append([cname,eid])
                        dis=levenshtein_distance(cname,fnamel)
                if(len(match_names)>0):
                    matched=match_names.pop()
                    anon[fname]=matched

    if(f == "Sheet_1.csv"): #In sheet one are the name of the people
        for row in csvfile:
            fname=row[9]
            if(fname in anon):
                a=1
               # print("we have it:")
               # print(fname+":"+anon[fname][0])
            else:
                match_names=list()
                if(fname):
                    print("csv:"+fname)
                    fnamel=fname.lower()
                    dis=1000
                    for row in allkey:
                        #print(row)
                        fn=row[0].strip()
                        ln=row[1].strip()
                        eid=int(row[2])
                        cname=fn.lower().strip()+" "+ln.lower().strip()
                        if(dis > levenshtein_distance(cname,fnamel) ):
                            match_names.append([cname,eid])
                            dis=levenshtein_distance(cname,fnamel)
                    if(len(match_names)>0):
                        matched=match_names.pop()
                        print("matched:"+matched[0])
                        anon[fname]=matched

#Replace all the key found in all file and replace by the number
for i in allcsv:
    fi = open("CSV/"+i, 'r')
    data = fi.read()
    fi.close()
    for key in anon:
        #print(key+" : "+ str(anon[key][1]))
        data=data.replace(key,str(anon[key][1]))
    fo = open("ANO/"+i, 'w')
    fo.write(data)
    fo.close()
    
