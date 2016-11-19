import bs4 as bs
from urllib.request import urlopen
import re
import csv
from SMC_course_list import *
from gradeProcessing import *
from general import *
from ratemyprofessor import *
import json

URL = "http://isismc02.smc.edu/isisdoc/web_cat_sched_20163.html"
PROJECT_NAME = "ClassList"
CSV_CLASS_TABLE = 'classTable.txt'
CSV_GRADE_TABLES = ['Spring 2012.csv','Spring 2013.csv','Fall 2012.csv','Fall 2013.csv','Spring 2014.csv','Fall 2014.csv','Spring 2015.csv','Fall 2015.csv']
CSV_PROCESSED_GRADE_TABLE = 'gradeData.csv'
CSV_RATEMYPROFESSOR = 'ratemyprofessor.csv'
CSV_GRADE_ALL = 'allGrade.csv'
CSV_CLASS_LIST = 'ClassList.csv'
create_data_files(PROJECT_NAME, CSV_CLASS_TABLE)
create_data_files(PROJECT_NAME, CSV_PROCESSED_GRADE_TABLE)
create_data_files(PROJECT_NAME, CSV_RATEMYPROFESSOR)
create_data_files(PROJECT_NAME, CSV_GRADE_ALL)
create_data_files(PROJECT_NAME, CSV_CLASS_LIST)
RATEMYPROFESSOR_URL = 'http://www.ratemyprofessors.com/find/professor/?page=1&queryoption=TEACHER&queryBy=schoolId&sid='
SCHOOL_ID = '1371'
CLASS_LIST=['0department','1course','2igetc','3courseID','4time','5location','6name']
# for files in CSV_GRADE_TABLES:
#     pre_process_grade_cvs(get_path(PROJECT_NAME, files))
Json_RATEMYPROFESSOR ='ratemyprofessor.json'
GRADE_ALL_JSON = 'allGrade.json'
JSON_NEW_DICT_PROFESSOR='newProfessor.json'
JSON_CHANGED_NAME_PROFESSOR="changedNameProfessor.json"
CSV_NEW_CLASS_LIST='finalClassList.csv'
JSON_NEW_CLASS_LIST='finalClassList.json'
JSON_EASYUI_NEW_CLASS_LIST='finalEasyuiClassList.json'
# read_Professor(PROJECT_NAME,Json_RATEMYPROFESSOR)
# read_grade(PROJECT_NAME,GRADE_ALL_JSON)
# read_class_list(PROJECT_NAME, CSV_CLASS_LIST)

def merge_professor_grade_classlist(project_name, json_ratemyprofessor, grade_all_json, csv_class_list, json_new_dic_professor,json_changed_name_dic_professor,csv_new_class_list):
    dic_professor = read_Professor(project_name,json_ratemyprofessor)
    dic_grade = read_grade(project_name, grade_all_json)
    list_class_list = read_class_list(project_name, csv_class_list)
    new_dic_professor={}
    changed_name_dic_professor={}
    new_list=[]
    # print(dic_grade)

    for course in list_class_list:
        course_info = []
        name = course[6].split()
        name_key = name[0]+' '
        if len(name) == 1:
            name_keys = [name[0]]
        elif len(name)>2:
            name_keys = [course[6], name[0] + ' ' + name[1] + ' ' + name[2],name[0] + '-' + name[1] + ' ' + name[2], name[0], name[0] + ' ' + name[1][0],
                         name[0] + ' ' + name[-1][0], name[0] + 's' + ' ' + name[1][0]]

        else:
            name_keys = [course[6],name[0],name[0] + ' ' + name[1][0],name[0] + ' ' + name[-1][0],name[0]+'s' + ' ' + name[1][0]]
        # print(name_key)
        grade_key = course[1] + ',' + course[6].upper()


        if grade_key in dic_grade:
            course_info = (course + dic_grade[grade_key])
        else:
            course_info = (course + [0,0,0,0,0,0,0,0,0])
        for key in name_keys:
            if key in dic_professor:
                name_key = key
                break


        if name_key in dic_professor:
            if len(dic_professor[name_key]) == 1:
                course_info += dic_professor[name_key][0]
                new_dic_professor[name_key]=[dic_professor[name_key][0]+[course[6]]]
                changed_name_dic_professor[course[6]]=[dic_professor[name_key][0]]
            else:
                added_to_dic = False
                # print (name_key, name_key not in new_dic_professor)
                if name_key not in new_dic_professor:
                    new_dic_professor[name_key] = []

                for professor in dic_professor[name_key]:

                    if len(professor[2]) >= 5:
                        text_length = 5
                    else:
                        text_length = len(professor[2])
                    ratemyprofessor_department = professor[2][:text_length]
                    classlist_department = course[0][:text_length]
                    if ratemyprofessor_department == classlist_department:
                        if added_to_dic:
                            print('same name in one department, added one ', course_info, 'deleted one ', professor)
                            if int(course_info[-1])<int(professor[-1]):
                                course_info=course_info[:-7]+professor
                            print('updated', course_info)
                            continue
                        added_to_dic =True
                        course_info += professor
                        new_dic_professor[name_key].append( [professor + [course[6]]])
                        # print(course[6],course[6] in changed_name_dic_professor)
                        if course[6] not in changed_name_dic_professor:
                            changed_name_dic_professor[course[6]] = []
                        changed_name_dic_professor[course[6]].append( professor)

                if not added_to_dic:
                    print('departments do not match, name:',course[6],' ratemypro ', dic_professor[name_key], course)
                    course_info += [0, 0, 0, 0, 0, 0, 0]
        else:
            course_info+=[0,0,0,0,0,0,0]
            print('name not in ratemyprofessor ',name_key ,course)
        new_list.append(course_info)
    with open(get_path(project_name,json_new_dic_professor), 'w') as jsonfile:
        json.dump(new_dic_professor,jsonfile)
    with open(get_path(project_name,json_changed_name_dic_professor),'w') as jsonfile:
        json.dump(changed_name_dic_professor,jsonfile)
    with open(get_path(project_name, csv_new_class_list),'w', newline='') as csvfile:
        csvwiter= csv.writer(csvfile,delimiter='\t')
        csvwiter.writerows(new_list)



# merge_professor_grade_classlist(PROJECT_NAME,Json_RATEMYPROFESSOR,GRADE_ALL_JSON,CSV_CLASS_LIST,JSON_NEW_DICT_PROFESSOR,JSON_CHANGED_NAME_PROFESSOR,CSV_NEW_CLASS_LIST)

def read_final_class_list(project_name,new_class_list):
    with open(get_path(project_name,new_class_list),newline='') as csvfile:
        csvdata= csv.reader(csvfile,delimiter='\t')
        # for line in csvdata:
        #     if len(line)!=23:
        #         print(line)
        #     print(line)
        # print(list(csvdata))
        return list(csvdata)

def csv_to_json(project_name,json_new_class_list):
    list = []
    pk=1
    finalCourseList = read_final_class_list(PROJECT_NAME,CSV_NEW_CLASS_LIST)
    print(finalCourseList)
    for course in finalCourseList:
        coursedict = {}
        coursedict['department_text'] = course[0]
        coursedict['course_text']=course[1]
        coursedict['igetc_text'] = course[2]
        coursedict['session_id'] = int(course[3])
        coursedict['schedule_text'] = course[4]
        coursedict['location_text'] = course[5]
        coursedict['instructor_text'] = course[6]
        coursedict['grade_A_num'] = int(course[7])
        coursedict['grade_B_num'] = int(course[8])
        coursedict['grade_C_num'] = int(course[9])
        coursedict['grade_P_num'] = int(course[10])
        coursedict['grade_total_num'] = int(course[11])
        coursedict['grade_A_rate'] = int(course[12])
        coursedict['grade_gt_B_rate'] = int(course[13])
        coursedict['grade_gt_C_rate'] = int(course[14])
        coursedict['grade_gt_P_rate'] = int(course[15])
        coursedict['rating_num_text'] = course[16]
        coursedict['url_text'] = course[17]
        coursedict['instructor_department_text'] = course[18]
        coursedict['lname_text'] = course[19]
        coursedict['fname_text'] = course[20]
        coursedict['tid_id'] = int(course[21])
        coursedict['votes_num'] = int(course[22])
        list.append({"model":"poos.CourseList",'pk':pk,'fields':coursedict})
        print(coursedict)
        pk +=1

    with open(get_path(project_name,json_new_class_list),'w') as jsonfile:
        json.dump(list,jsonfile)


def csv_to_easyui_json(project_name, json_new_class_list):
    list = []
    pk = 1
    finalCourseList = read_final_class_list(PROJECT_NAME, CSV_NEW_CLASS_LIST)
    # print(finalCourseList)
    for course in finalCourseList:
        coursedict = {}
        coursedictlist=[{},{},{}]
        coursedict['Department'] = course[0]
        coursedict['Course'] = course[1]+' '

        coursedict['Session_id'] = int(course[3])
        if len(course[4].split()) == 1:
            coursedict['Time'] = course[4].split()[0]
            coursedict['Weekday'] = 'None'
        else:
            coursedict['Time'] = course[4].split()[0]
            coursedict['Weekday'] = course[4].split()[1]
        coursedict['Location'] = course[5]
        coursedict['InstructorName'] = course[6]
        # coursedict['grade_A_sum'] = int(course[7])
        # coursedict['grade_B_sum'] = int(course[8])
        # coursedict['grade_C_sum'] = int(course[9])
        # coursedict['grade_P_sum'] = int(course[10])
        coursedict['numberOfStudents'] = int(course[11])
        coursedict['grade_A_rate'] = int(course[12])
        coursedict['grade_gt_B_rate'] = int(course[13])
        coursedict['grade_gt_C_rate'] = int(course[14])
        coursedict['grade_gt_P_rate'] = int(course[15])
        try:
            coursedict['rating'] = float(course[16])
        except:
            coursedict['rating'] = 0
        # coursedict['url_text'] = course[17]
        # link

        # coursedict['instructor_department_text'] = course[18]
        # coursedict['lname_text'] = course[19]
        # coursedict['fname_text'] = course[20]
        # coursedict['tid_id'] = int(course[21])
        # url = course[17]
        coursedict['votes_num'] = int(course[22])
        temp = '' + course[2]
        temp = temp.split(',')
        # if course[1]=="HIST 15":
        #     print(len(temp))
        if len(temp) == 1:
            if len(temp[0])>3:
                coursedict['igetcFilter'] = course[2]
                coursedict['igetc'] = course[2]
            elif(len(course[2])==0):
                coursedict['igetcFilter'] = ''
                coursedict['igetc'] = ''
            else:
                coursedict['igetcFilter'] = course[2][0]
                coursedict['igetc'] = course[2]
        else:
            for i in range(len(temp)):
                # print(len(temp),temp)
                if i == 0:

                    if len(temp[0]) > 3:
                        coursedict['igetcFilter'] = temp[i]
                        coursedict['igetc'] = course[2]
                    elif (len(course[2]) == 0):
                        coursedict['igetcFilter'] = ''
                        coursedict['igetc'] = ''
                    else:
                        coursedict['igetcFilter'] = temp[i][0]
                        coursedict['igetc'] = course[2]
                # else:
                #     # print(i)
                #     coursedictlist[i] = coursedict.copy()
                #     # if len(course[17]) > 5:
                #     #     coursedictlist[i] = "<a href='" + course[17] + "'>" + course[6] + "</a>"
                #     # else:
                #     #     coursedictlist[i] = course[6]
                #
                #     if len(temp) == 1:
                #         if len(temp[0]) > 3:
                #             coursedictlist[i]['igetcFilter'] = temp[i]
                #             coursedictlist[i]['igetc'] = course[2]
                #         elif (len(course[2]) == 0):
                #             coursedictlist[i]['igetcFilter'] = ''
                #             coursedictlist[i]['igetc'] = ''
                #         else:
                #             coursedictlist[i]['igetcFilter'] = temp[i][0]
                #             coursedictlist[i]['igetc'] = course[2]

        if len(course[17]) >5:
            coursedict['Instructor'] = "<a href='" + course[17] + "'>" + course[6] + "</a>"
        else:
            coursedict['Instructor'] = course[6]

        # coursedict['Instructor'] = "<a href='" + course[17] + "'>" + course[6] + "</a>" + ' ' + course[3]+''+coursedict['Time'] + ' ' + coursedict['Weekday'] + ' ' + coursedict['Location']
        list.append(coursedict)
        for x in coursedictlist:
            if len(x)!=0:
                list.append(x)

    with open(get_path(project_name, json_new_class_list), 'w') as jsonfile:
        json.dump(list, jsonfile)
# read_final_class_list(PROJECT_NAME,CSV_NEW_CLASS_LIST)
# csv_to_json(PROJECT_NAME,JSON_NEW_CLASS_LIST)
csv_to_easyui_json(PROJECT_NAME,JSON_EASYUI_NEW_CLASS_LIST)
