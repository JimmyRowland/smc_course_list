from urllib.request import urlopen
import json
from math import ceil
import csv
from general import *

RATEMYPROFESSOR_URL = 'http://www.ratemyprofessors.com/find/professor/?queryoption=TEACHER&queryBy=schoolId&sid='
SCHOOL_ID = '1371'
PROJECT_NAME = "ClassList"
CSV_RATEMYPROFESSOR = 'ratemyprofessor.csv'
Json_RATEMYPROFESSOR ='ratemyprofessor.json'


def get_rating_from_ratemyprofessor(baseURL, schoolID, path):
    result = []
    pages = 1
    maxpages = 0
    urlpage= '&page='
    url = baseURL+schoolID+urlpage+str(pages)
    response = urlopen(url).read().decode("utf-8")
    data = json.loads(response)
    maxpages = ceil(int(data['searchResultsTotal'])/20)
    for num in range(maxpages):
        # if num == 2:
        #     break
        url = baseURL + schoolID + urlpage + str(pages)
        response = urlopen(url).read().decode("utf-8")
        data = json.loads(response)
        pages += 1
        print(url)
        for professors in data['professors']:
            result.append([professors['tLname']+' '+professors['tFname'][0], professors['overall_rating'], "http://www.ratemyprofessors.com/ShowRatings.jsp?tid="+str(professors["tid"]),professors['tDept'],professors['tLname'],professors['tFname'],professors["tid"],professors["tNumRatings"]])
            result.append([professors['tLname'] + ' ' + professors['tFname'][0], professors['overall_rating'],
                           "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(professors["tid"]),
                           professors['tDept'], professors['tLname'], professors['tFname'], professors["tid"],
                           professors["tNumRatings"]])
            # print(result)

        # print(data)
        # print(data['professors'][0])
        # print(data['professors'][19])
        # print(maxpages)
    with open(path, 'w', newline='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter='\t')
        writeCSV.writerows(result)


def jsonProfessor(project_name, cvs_ratemyprofessor, json_ratemyprofessor):

    with open(get_path(project_name, cvs_ratemyprofessor), newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        dic={}
        for row in readCSV:
            if row[0] not in dic:
                dic[row[0]]=[row[1:]]
            else:
                dic[row[0]].append(row[1:])
                print(dic[row[0]])
    with open(get_path(project_name,json_ratemyprofessor), 'w') as jsonfile:
        json.dump(dic, jsonfile)


def read_Professor(project_name,  json_ratemyprofessor):
    with open(get_path(project_name,json_ratemyprofessor)) as jsonfile:
        dic = json.load(jsonfile)
        # print(dic)
        return dic

# get_rating_from_ratemyprofessor(RATEMYPROFESSOR_URL, SCHOOL_ID, get_path(PROJECT_NAME,CSV_RATEMYPROFESSOR))
# jsonProfessor(PROJECT_NAME,CSV_RATEMYPROFESSOR,Json_RATEMYPROFESSOR)
# read_Professor(PROJECT_NAME,Json_RATEMYPROFESSOR)