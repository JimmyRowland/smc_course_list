import bs4 as bs
from urllib.request import urlopen
from general import *
import re
import csv


URL = ["https://isiscc.smc.edu/isisdoc/web_cat_sched_20190.html",
       # "https://isiscc.smc.edu/isisdoc/web_cat_sched_20191.html"
       ]

PROJECT_NAME = "ClassList"
PATH = "./"+PROJECT_NAME+"/classTable.txt"
CSV_CLASS_TABLE = 'classTable.txt'
CSV_GRADE_TABLES = ['Grade Distribution Spring 2012.csv','Grade Distribution Spring 2013.csv','Grade Distribution Fall 2012.csv','Grade Distribution Fall 2013.csv','Santa Monica College - Grade Distribution Spring 2014.csv','Santa Monica College - Grade Distribution Fall 2014.csv','Santa Monica College - Grade Distribution Spring 2015.csv','Fall 2015 Grade Distribution- Report.csv']
CSV_PROCESSED_GRADE_TABLE = 'gradeData.csv'
create_data_files(PROJECT_NAME, CSV_CLASS_TABLE)
create_data_files(PROJECT_NAME, CSV_PROCESSED_GRADE_TABLE)
CSV_CLASS_LIST = 'ClassList.csv'
CLASS_LIST=['department','course','department','time','location','name']
localFile= [
    './officialCourseListHTML/SMC Course Schedule 2019 winter.html',
    './officialCourseListHTML/SMC Course Schedule 2019 spring.html'
]

def get_course_list(localFile, project_name, csv_class_list):
    data = []
    for file in localFile:
        # response = urlopen(file).read()
        # print(response)
        # html = bs.BeautifulSoup(response, 'lxml')
        html = bs.BeautifulSoup(open(file, encoding="utf-8").read(), "lxml")
        # print(html)
        semester = ''
        department = ''
        course = ''
        unit = ''
        igect = ''
        courseInfo = ""
        # infoIndex = 0
        # igetcDic = {}
        sectionNum = ''
        location = ''
        professor = ''
        time = ''
        date = ''
        departmentDescriptions=''
        UC = False
        CSU = False
        transfer = ''
        prerequisite = 'None'
        for div in html.find_all('div'):
            # print(div)
            if div.get('id')=='container':
                # for table in div:
                for tag in div:
                    # print("container", tag)
                    # print(tag.name)
                    # print("something")
                    # department=''
                    departmentDescriptions = ''


                    if tag.name == 'h1':
                        print("semester", tag.text)
                        regex = re.compile(r"(.*) Schedule of Classes")
                        matches = re.findall(regex, tag.text)
                        if (len(matches)):
                            semester = matches[0]
                            print(semester)
                    elif tag.name == 'h2':
                        print(tag)
                        department = tag.text
                    elif tag.name == 'div' and tag.get('tabindex') == '-1':

                        course = ''
                        unit = 0
                        UC = False
                        CSU = False
                        transfer = ''
                        prerequisite = 'None'
                        igect = ''
                        courseInfo = ""


                        for index, classTag in enumerate(tag):
                            # sectionNum = ''
                            # location = ''
                            # professor = ''
                            # time = ''
                            # date = ''
                            # print(classTag)
                            try:
                                if classTag.name == 'h3':
                                    course = classTag.text.split(',')[0]
                                    if 'unit' in classTag.text:
                                        regex = re.compile(r".*([1-9]) unit.*")
                                        matches = re.findall(regex, classTag.text)
                                        print('unitMatches', matches, matches[0].isdigit())
                                        if matches[0].isdigit():
                                            print("unit@", unit, matches)
                                            unit = matches[0]
                                        else:
                                            unit = 0
                                            print("unit error", classTag.text, matches)
                                        # unit = matches[0] if matches[0] != '' else 0
                                        # unit=classTag.text.strip().split(' ')[-2]
                                    else:
                                        unit = 0
                                    # print(course)
                                    print("course ", course, "unit!", unit)
                                elif isinstance(classTag, bs.NavigableString):
                                    continue
                                elif "Transfer" in classTag.getText():
                                    if 'UC' in classTag.text:
                                        UC = True
                                        transfer+='UC '
                                    if 'CSU' in classTag.text:
                                        CSU = True
                                        transfer+='CSU'
                                elif "Prerequisite" in classTag.text:
                                    regex = re.compile(r"Prerequisite: (.*).")
                                    matches = re.findall(regex, classTag.text)
                                    prerequisite = matches[0]
                                elif classTag.name == 'p' and not classTag.has_attr('class'):
                                    courseInfo = classTag.text
                                elif classTag.name == 'p' and classTag.attrs.get("class") == ['course']:
                                    print("!!!!!!!!!!!!!!!!")
                                    for infoClassTag in classTag.find_all('span'):
                                        # print("????????")
                                        print(infoClassTag)
                                        if infoClassTag.attrs.get('class') == ["course-number"]:
                                            sectionNum = infoClassTag.text
                                            regex = re.compile(r"Course Number:(.*)")
                                            matches = re.findall(regex, sectionNum)
                                            sectionNum = matches[0]
                                        elif infoClassTag.get('class') == ['time']:
                                            temp = infoClassTag.text.split(' ')
                                            date = temp.pop()
                                            time = "".join(temp)
                                            regex = re.compile(r"Time:(.*)")
                                            matches = re.findall(regex, time)
                                            time = matches[0]
                                        elif infoClassTag.get('class') == ['location']:
                                            location = infoClassTag.text
                                            regex = re.compile(r"Location:(.*)")
                                            matches = re.findall(regex, location)
                                            location = matches[0]
                                        elif infoClassTag.get('class') == ['instructor']:
                                            professor = infoClassTag.getText()
                                            regex = re.compile(r"Instructor:(.*)")
                                            matches = re.findall(regex, professor)
                                            professor = matches[0]
                                elif classTag.name == 'p' and classTag.get('class') == ['course', 'second-line']:
                                    for infoClassTag in classTag.find_all('span'):
                                        if infoClassTag.get('class') == ['time']:
                                            temp = infoClassTag.text.replace("Time:",'').split(' ')
                                            date = date + '\n' + temp.pop()
                                            time = time + '\n' + "".join(temp)
                                        if infoClassTag.get('class') == 'location':
                                            location = location + '\n' + infoClassTag.text.replace("Location:",'')
                                    data.pop()
                                elif "IGETC" in classTag.text:
                                    regex = re.compile(r"[1-9]+[A-Z]?")
                                    matches = re.findall(regex, classTag.text)
                                    if 'Foreign Language' in classTag.text:
                                        matches.append('Foreign Language')
                                    igect = ','.join(matches)

                                else:
                                    print("else")
                                    print(classTag
                                          , type(classTag)
                                          , professor
                                          , sectionNum
                                          # , classTag.get("class"),classTag.attrs.values(),classTag.attrs.get("class")
                                          )
                                if len(professor) and classTag.attrs.get("class")[0] == 'course':
                                    print('push', classTag)
                                    data.append({
                                        'department': department,
                                        'course': course,
                                        'igetc': igect,
                                        "section": sectionNum,
                                        "time+date": time + " " + date,
                                        "location": location,
                                        "professor": professor,
                                        # 'departmentDescription': departmentDescriptions,
                                        # "UC": UC,
                                        # "CSU": CSU,
                                        'transfer': transfer,
                                        # "prerequisite": prerequisite,
                                        'courseDescription': courseInfo,
                                        "time": time,
                                        "date": date,

                                        "semester": semester,

                                        "unit": unit

                                    })
                                # data.append({
                                #     'department': department,
                                #     'course': course,
                                #     'departmentDescription': departmentDescriptions,
                                #     "UC": UC,
                                #     "CSU": CSU,
                                #     'transfer': transfer,
                                #     'igetc': igect,
                                #     # "prerequisite": prerequisite,
                                #     # 'courseDescription': courseInfo,
                                #     "time": time,
                                #     "date": date,
                                #     "location": location,
                                #     "professor": professor,
                                #     "semester": semester,
                                #     "section": sectionNum
                                #
                                # })
                            except Exception as e:
                                print("error", e)
                                print(classTag
                                      # , type(classTag)
                                      , classTag.get("class")
                                      # , classTag.attrs.values()
                                      , classTag.attrs.get("class")
                                      # , classTag.find_all("span")
                                      )






        # for div1 in html.find_all('div'):
        #     for x in div1.find_all('div'):
        #         if x.name == 'h1':
        #             regex = re.compile(r"(.*) Schedule of Classes")
        #             matches = re.findall(regex, x.text)
        #             if (len(matches)):
        #                 semester = matches[0]
        #                 print(semester)
        #         if x.name == 'h2':
        #             apartment = x.text
        #             course = ''
        #             igect = ''
        #         if x.name == 'div':
        #             for row in x:
        #                 print(row)
        #                 print(row.get('class'))
        #                 if x.name == 'h3':
        #                     # print(x.text)
        #                     course = x.text.split(',')[0]
        #                     print(course)
        #                     igect = ''
        #                 elif row.get('class')=='course':
        #                     string = str(x)
        #                     if len(string) == 4 and string.isdigit():
        #                         infoIndex = 1
        #                         courseInfo.append(string)
        #                     elif infoIndex == 1 or infoIndex == 2:
        #                         courseInfo.append(string)
        #                         infoIndex += 1
        #                     elif infoIndex == 3:
        #                         infoIndex = 0
        #                         courseInfo.append(string)
        #                         # print([apartment, course, igect])
        #                         # print(string, courseInfo)
        #                         data.append([apartment, course, igect] + courseInfo + [semester])
        #                         courseInfo = []
        #                     elif "IGETC" in string:
        #
        #                         regex = re.compile(r"[1-9]+[A-Z]?")
        #                         matches = re.findall(regex, string)
        #                         # print(matches,string)
        #                         # for match in matches:
        #                         #     if match[0] not in matches:
        #                         #         matches.append(match[0])
        #                         #
        #                         if 'Foreign Language' in string:
        #                             matches.append('Foreign Language')
        #                         # for match in matches:
        #                         #     if match not in igetcDic:
        #                         #         igetcDic[match] = [course]
        #                         #     else:
        #                         #         if course not in igetcDic[match]:
        #                         #             igetcDic[match].append(course)
        #                         igect = ','.join(matches)
        # # print(igetcDic)

    with open(get_path(project_name,csv_class_list),'w',newline='') as csvfile:
        keys = data[0].keys()
        writeCSV = csv.DictWriter(csvfile,keys,delimiter='\t')
        writeCSV.writerows(data)


def read_class_list(project_name, csv_class_list):
    with open(get_path(project_name,csv_class_list),newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        # print(readCSV)
        return list(readCSV)
def courseDescriptionForApplication(localFile, project_name, csv_class_list):
    with open(get_path(project_name,csv_class_list),'r') as courseDesFile:
        readCourseDesFile = csv.reader(courseDesFile,delimiter='\t')
        # print("readCourseDesFilelist",list(readCourseDesFile))
        something=list(readCourseDesFile)
        result=[]
        print("afterlist",something)
        with open("/mnt/9EA6C149A6C1231F/OneDrive/ubuntu download/tabula-rwservlet (1).csv", 'r') as coursesfile:
            readCourses = csv.reader(coursesfile)
            courses=list(readCourses)


            for course in courses:
                # print(course[-1])
                i = 0
                while(i<len(something)):
                    # print("test",i,something[i], course[0])
                    if something[i][1]==course[0]:
                        resultString = f'<h2><a href="https://smccis.smc.edu/isisdoc/web_cat_sched_20191.html#{"-".join(course[0].split(" "))}" >{course[0]}</a>, {something[i][-1]} Unit</h2><p>{something[i][8]}</p>'
                        result.append([resultString])
                        print(resultString)
                        i+=1
                        break
                    i+=1

            with open("./htmlfile.cvs","w",newline='') as htmlfile:
                writeCSV = csv.writer(htmlfile, delimiter='\t')
                writeCSV.writerows(result)
            print(list(readCourses))
        # print(readCourseDesFile)

        # print(list(readCourseDesFile)[0])

get_course_list(localFile,PROJECT_NAME,CSV_CLASS_LIST)
# courseDescriptionForApplication(localFile,PROJECT_NAME,CSV_CLASS_LIST)
# read_class_list(PROJECT_NAME, CSV_CLASS_LIST)


