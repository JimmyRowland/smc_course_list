import csv
from general import *
from math import ceil
import json

CSV_GRADE_TABLES = ['Spring 2012.csv','Spring 2013.csv','Fall 2012.csv','Fall 2013.csv','Spring 2014.csv','Fall 2014.csv','Spring 2015.csv','Fall 2015.csv']
PROJECT_NAME = "ClassList"
CSV_GRADE_ALL = 'allGrade.csv'
GRADE_ALL_JSON = 'allGrade.json'

def pre_process_grade_cvs(path):
    with open(path, newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        nextDepartment = False
        department = ''
        course = ''
        data = []
        instructor = ''
        grade_A = ''
        grade_B = ''
        grade_C = ''
        grade_P = ''
        total = ''

        # x = 0
        # for row in readCSV:
        #     if x==10:
        #         break
        #     x+=1
        #     print(row[5])

        for row in readCSV:
            if row[0] == 'Department':
                p_index = row.index('P')-row.index('A')
                continue
            if len(row[4]) > 0:
                if len(row[0]) > 0:
                    department = row[0]
                if len(row[4]) == 4 and row[4].isdigit():
                    if row[3] !='':
                        course = row[2] + ' ' + row[3]
                    elif row[2]!='':
                        course = row[2]
                    temp = 5
                    if not row[temp+1].isdigit():
                        instructor = row[temp] + ' ' +row[temp+1]
                        temp += 1
                    else:
                        instructor = row[temp]
                    grade_A = row[temp+1]
                    grade_B = row[temp+2]
                    grade_C = row[temp+3]
                    grade_P = row[temp+p_index]
                    total = row[-2]
                elif len(row[3]) == 4 and row[3].isdigit():
                    if row[2] != '':
                        course = row[2]
                    temp = 4
                    if not row[temp + 1].isdigit():
                        instructor = row[temp] + ' ' + row[temp + 1]
                        temp += 1
                    else:
                        instructor = row[temp]
                    grade_A = row[temp + 1]
                    grade_B = row[temp + 2]
                    grade_C = row[temp + 3]
                    grade_P = row[temp + p_index]
                    total = row[-2]

                else:
                    if row[3] != '':
                        course = row[2]
                    temp = 4
                    if not row[temp + 1].isdigit():
                        instructor = row[temp] + ' ' + row[temp + 1]
                        temp += 1
                    else:
                        instructor = row[temp]
                    grade_A = row[temp + 1]
                    grade_B = row[temp + 2]
                    grade_C = row[temp + 3]
                    grade_P = row[temp + p_index]
                    total = row[-2]
                if row[-1]!='':
                    total = row[-1]

                courseID = course + "," + instructor
                data.append([department, courseID, course, instructor, grade_A, grade_B, grade_C, grade_P, total])
            else:
                print(row)

    with open(path, 'w', newline='') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter='\t')
        writeCSV.writerows(data)


def merge_grade_file(fileList, projectName, outputFileName):
    dictionary={}
    for file in fileList:
        path = get_path(projectName, file)
        with open(path, newline='') as csvfile:
            readCSV = csv.reader(csvfile, delimiter='\t')
            for row in readCSV:
                for index in range(5):
                    # print(row[index+4])
                    # print(row[-1],row[-2], len(row))
                    # print(path)
                    if row[-1] == '':
                        print (row)
                        print(path)
                        continue
                    if row[index+4] == '':
                        row[index + 4] = 0
                    else:
                        row[index + 4] = int(row[index + 4])

                if row[1] not in dictionary:
                    dictionary[row[1]] = [row[-5],row[-4],row[-3],row[-2],row[-1]]
                else:
                    for index in range(5):
                        dictionary[row[1]][index] += row[index-5]
    for key in dictionary:
        sum = 0
        for index in range(4):
            sum += dictionary[key][index]
            dictionary[key].append((ceil((sum/dictionary[key][4])*100)))
            # print(dictionary[key])
    path = get_path(projectName, outputFileName)
    with open(path, "w") as jsonFile:
        json.dump(dictionary, jsonFile)
    # with open(path, 'wb') as csv_file:
    #     writer = csv.writer(csv_file, delimiter='\t')
    #     # writer.writerow(dictionary)
    #     print(dictionary)
    #     # for key, value in dictionary.items():
    #     #     # for index in range(9):
    #     #     #     value[index] = str(value[index])
    #     #     writer.writerow(value)

def read_grade(project_name, file_name):
    path = get_path(project_name, file_name)
    with open(path) as json_data:
        dic = json.load(json_data)
        # print(dic)
        return dic



# merge_grade_file(CSV_GRADE_TABLES,PROJECT_NAME,GRADE_ALL_JSON)
# for files in CSV_GRADE_TABLES:
#     pre_process_grade_cvs(get_path(PROJECT_NAME, files))
# read_grade(PROJECT_NAME,GRADE_ALL_JSON)

