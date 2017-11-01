import bs4 as bs
from urllib.request import urlopen
from general import *
import re
import csv


URL = ["https://isiscc.smc.edu/isisdoc/web_cat_sched_20181.html","https://isiscc.smc.edu/isisdoc/web_cat_sched_20180.html"]

PROJECT_NAME = "ClassList"
PATH = "./"+PROJECT_NAME+"/classTable.txt"
CSV_CLASS_TABLE = 'classTable.txt'
CSV_GRADE_TABLES = ['Grade Distribution Spring 2012.csv','Grade Distribution Spring 2013.csv','Grade Distribution Fall 2012.csv','Grade Distribution Fall 2013.csv','Santa Monica College - Grade Distribution Spring 2014.csv','Santa Monica College - Grade Distribution Fall 2014.csv','Santa Monica College - Grade Distribution Spring 2015.csv','Fall 2015 Grade Distribution- Report.csv']
CSV_PROCESSED_GRADE_TABLE = 'gradeData.csv'
create_data_files(PROJECT_NAME, CSV_CLASS_TABLE)
create_data_files(PROJECT_NAME, CSV_PROCESSED_GRADE_TABLE)
CSV_CLASS_LIST = 'ClassList.csv'
CLASS_LIST=['department','course','courseID','time','location','name']


def get_course_list(urllist,project_name,csv_class_list):
    data = []
    for url in urllist:
        response = urlopen(url).read()
        html = bs.BeautifulSoup(response, 'lxml')

        apartment = ''
        course = ''
        igect = ''
        semester=''
        courseInfo = []
        infoIndex = 0
        igetcDic = {}
        for tr in html.find_all('tr'):
            for td in tr.find_all("td"):
                for x in td:
                    if x.name =='h1':
                        regex = re.compile(r"SMC (.*) Schedule of Classes")
                        matches = re.findall(regex, x.text)
                        if(len(matches)):
                            semester = matches[0]
                            print(semester)
                        else:
                            apartment = x.text
                            course = ''
                            igect = ''
                    # if x.name == 'h2':
                    #     apartment = x.text
                    #     course = ''
                    #     igect = ''
                    elif x.name == 'a':
                        course = ' '.join(x.get('name').split())
                        igect = ''
                    else:
                        string = str(x)
                        if len(string) == 4 and string.isdigit():
                            infoIndex = 1
                            courseInfo.append(string)
                        elif infoIndex == 1 or infoIndex == 2:
                            courseInfo.append(string)
                            infoIndex += 1
                        elif infoIndex == 3:
                            infoIndex = 0
                            courseInfo.append(string)
                            # print([apartment, course, igect])
                            # print(string, courseInfo)
                            data.append([apartment, course, igect] + courseInfo + [semester])
                            courseInfo = []
                        elif "IGETC" in string:

                            regex = re.compile(r"[1-9]+[A-Z]?")
                            matches = re.findall(regex, string)
                            # print(matches,string)
                            # for match in matches:
                            #     if match[0] not in matches:
                            #         matches.append(match[0])
                            #
                            if 'Foreign Language' in string:
                                matches.append('Foreign Language')
                            # for match in matches:
                            #     if match not in igetcDic:
                            #         igetcDic[match] = [course]
                            #     else:
                            #         if course not in igetcDic[match]:
                            #             igetcDic[match].append(course)
                            igect = ','.join(matches)
    # print(igetcDic)
    with open(get_path(project_name,csv_class_list),'w',newline='') as csvfile:
        writeCSV = csv.writer(csvfile,delimiter='\t')
        writeCSV.writerows(data)


def read_class_list(project_name, csv_class_list):
    with open(get_path(project_name,csv_class_list),newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        # print(readCSV)
        return list(readCSV)


# get_course_list(URL,PROJECT_NAME,CSV_CLASS_LIST)
# read_class_list(PROJECT_NAME, CSV_CLASS_LIST)


