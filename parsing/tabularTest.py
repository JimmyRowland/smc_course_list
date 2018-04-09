import tabula
import textract
import re
import pandas
# import os
import glob
# import inspect
import pickle
from general import *
import pdfquery
from pdfquery.cache import FileCache
from math import ceil
import codecs
import numpy



import csv
from general import *
import json

CSV_GRADE_TABLES = ['Spring 2012.csv','Spring 2013.csv','Fall 2012.csv','Fall 2013.csv','Spring 2014.csv','Fall 2014.csv','Spring 2015.csv','Fall 2015.csv']
PROJECT_NAME = "ClassList"
CSV_GRADE_ALL = 'allGrade.csv'
GRADE_ALL_JSON = 'allGrade.json'



def getColumnCoordinatesSemesterYear(path):

    pdf = pdfquery.PDFQuery(path,parse_tree_cacher=FileCache("/tmp/"))
    pdf.load(0)


    lable = pdf.pq('LTTextLineHorizontal:contains("Santa Monica College")').text()
    regex = re.compile(r"\d{4}")
    year = re.search(regex, lable).group()
    if "Spring" in lable:
        semester = "Spring"
    elif "Fall" in lable:
        semester = "Fall"
    else:
        semester = "error"


    def getCenter(bbox):
        x = (float(bbox.attr("x0")) + float(bbox.attr("x1"))) / 2
        y = (float(bbox.attr("y0")) + float(bbox.attr("y1"))) / 2
        return [x, y]
    def align(bbox):
        # print(bbox.text())
        leftorright=''
        def leftCenterRight(x0,left):
            # print(left)
            counter=2
            temp=float(bbox.attr(x0))
            # for z in bbox.items():
                # print(z)
            for x in [float(i.attr(x0)) for i in bbox.items()]:
                # print(x,temp)
                if abs(x-temp)<2:
                    counter+=1
                    # if counter >4:
                    #
                    #     return left
                # else:
                #     counter-=1
                #     if counter < 0:
                #         return ''
                temp=x
            # print(counter)
            return counter
        # leftorright=leftCenterRight('x0','left')
        # if leftorright == '':
        #     leftCenterRight('x1', 'right')
        # print(leftorright)
        # if leftorright =='':
        #     return 'center'
        # else:
        #     return leftorright
        leftCount=leftCenterRight('x0','left')
        # if leftCount <5:
        #     return 'left'
        if leftCount>leftCenterRight('x1', 'right'):

            return  'left'
        else:
            return 'right'








    pageWidth = float(pdf.pq('LTPage').attr("x1"))
    pageHeight=float(pdf.pq('LTPage').attr("y1"))
    department = pdf.pq('LTTextLineHorizontal:contains("Department")')
    section=department = pdf.pq('LTTextLineHorizontal:contains("Section")')
    departmentCenter = getCenter(department)
    firstRow = pdf.pq('LTTextLineHorizontal:overlaps_bbox("0,%s,%s,%s")' % (
    departmentCenter[1], pageWidth, departmentCenter[1] + 0.1))
    rowSection=pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,0,%s,%s")' % (
    section.attr('x0'),section.attr('x1'), section.attr('y1')))

    y0table=min([float(o.attr('y0')) for o in rowSection.items()])
    # print(y0table, rowSection.attr('y1'), rowSection.text())
    x0FirstRow=[]
    columnsName=[]
    # x0FirstRow = [float(i.attr('x1')) for i in firstRow.items()]
    if('2015'in year and 'Fall' in semester):
        for i in firstRow.items():
            columnsName.append(i.text())
            if "Instructor" in i.text():
                # print("Instructor")
                continue
            elif 'Department' in i.text():
                x1Department=float(i.attr("x1"))
            elif 'Subject' in i.text():
                x0Subject=float(i.attr("x0"))
                x0FirstRow.append(float(i.attr("x1"))+5)
            elif 'Course' in i.text():

                continue

            elif "A" in i.text() or "Section" in i.text():
                # print("A")
                x0FirstRow.append(float(i.attr("x0"))-3)
                x0FirstRow.append(float(i.attr("x1")))
            else:
                x0FirstRow.append(float(i.attr("x1")))
        x0FirstRow.append((x0Subject+x1Department)/2)
    # elif('Spring' in semester):
    else:
        columnResult=[]

        for i in firstRow.items():
            columnsName.append(i.text())

            # if ("Department" in i.text()):
            #     print("Department")
            #     continue
            # elif ("Subject" in i.text() or "Course" in i.text() or "Section" in i.text() or "Instructor" in i.text()):
            #     print("CourseSection")
            #     x0FirstRow.append(float(i.attr("x0")) - 3)
            #
            #
            # elif ("A" in i.text()):
            #     x0FirstRow.append(float(i.attr("x0"))-10)
            #     x0FirstRow.append(float(i.attr("x1")))
            # else:
            #     x0FirstRow.append(float(i.attr("x1")))
            columns = pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (
                i.attr('x0'), y0table-4 ,i.attr('x1'), float(i.attr('y0'))-4))
            # print(i.attr('x0'), y0table-4 ,i.attr('x1'), float(i.attr('y0'))-4,columns.text())
            columnsTest=[]

            for x in columns.items():
                xCenter= getCenter(x)
                # print(x.text())
                test= pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s,%s,%s,%s")' % (
                    xCenter[0],y0table-4 , xCenter[0]+0.1, float(i.attr('y0'))-4))
                # print(test.text())
                if len(test)<len(columns) and test not in columnsTest:
                    print(test.text())
                    columnsTest.append(test)
            if len(columnsTest)==0:
                if len(columns):
                    columnsTest.append(columns)
                else:
                    columnsTest.append(i)

                x0FirstRow.append(float(i.attr('x0')))
                x0FirstRow.append(float(i.attr('x1')))
            else:
                for y in columnsTest:
                    # print(len(columnsTest),y.text())
                    minx0=min([float(bbox.attr('x0')) for bbox in y.items()])
                    if minx0 not in x0FirstRow:
                        x0FirstRow.append(minx0)
                    maxx0=max([float(bbox.attr('x1')) for bbox in y.items()])
                    if maxx0 not in x0FirstRow:
                        x0FirstRow.append(maxx0)
                    # print(i.text(),x0FirstRow[-2],x0FirstRow[-1])
            columnResult+=columnsTest
            # for u in columnsTest:
                # print('uuuuuu',u.text())
        position=[]
        columnResult.sort(key=lambda x :float(x.attr('x0')))
        for bbox in columnResult:
            # if len(bbox):
            # print(align(bbox))
            position.append(align(bbox))
        print(len(position),position)
        position[0]='left' #long department name
        position[3] = 'left' #long course name
        x0FirstRow.sort()
        rowTemp=[]
        rowTemp.append(x0FirstRow[0])
        for num in range(0,len(x0FirstRow)-2,2):
            # print(num)
            # print(position[int(num/2)],position[int(num/2+1)]=='right')
            if(position[int(num/2)]=='right' and position[int(num/2+1)]=='right'):
                rowTemp.append(x0FirstRow[num + 1] + (x0FirstRow[num + 2] - x0FirstRow[num + 1]) * 1 / 10)
            else:
                rowTemp.append(x0FirstRow[num+1]+(x0FirstRow[num+2]-x0FirstRow[num+1])*9/10)
            # print(rowTemp[-1],x0FirstRow[num+1],x0FirstRow[num+2])
        x0FirstRow=rowTemp[1:]
        # print(len(x0FirstRow),x0FirstRow)










    # x0FirstRow.append(pageWidth)
    # x0FirstRow.append(0)
    x0FirstRow=[x for x in x0FirstRow]
    # print(columnsName)
    return [x0FirstRow,[year,semester]]


def getSemesterAndYear(texttemp):
    # print(dir(textract))
    # print(inspect.getsource(textract))
    text = textract.process('pdfFiles/Fall 2015 Grade Distribution- Report.pdf')
    # print(text)
    # print(str(text).split("\\n"))
    # print("df")
    # def write_file(path, data):
    #     with open(path, 'w') as f:
    #         f.write(data)
    # write_file("test.txt",str(text))

    regex = re.compile(r"\d{4}")
    year = re.search(regex, text).group()
    if "Spring" in text:
        semester = "Spring"
    elif "Fall" in text:
        semester = "Fall"
    else:
        semester = "error"
    # print(year, semester)
    return([year,semester])


def getTableDataToPickle(pathList):
    create_project_dir("picklepdfFiles")


    for path in pathList:
        columnCoordinatesSemesterYear=getColumnCoordinatesSemesterYear(path)
        columncoordinate = columnCoordinatesSemesterYear[0]
        year=columnCoordinatesSemesterYear[1][0]
        semester=columnCoordinatesSemesterYear[1][1]

        columncoordinate.sort()
        # temp=[79.095, 135.415, 195.91, 254.311, 335.386, 379.04, 403.338, 427.479, 451.73, 475.497, 500.562, 524.322, 551.782, 572.548, 596.632, 623.319, 660.992]
        # print(len(temp),temp)
        # columncoordinate=columncoordinate[1:]
        # print(len(columncoordinate),columncoordinate)
        # print(columncoordinate[1:])
        # df = tabula.read_pdf(path,pages=[22],silent=True,guess=False,columns=columncoordinate[2:])

        df = tabula.read_pdf(path,pages='all',silent=True,guess=False,columns=columncoordinate[0:])
        df["Year"]=year
        df["Semester"]=semester
        df.to_csv('test/'+path+'.csv')
        # print(df)
        # print([20+x for x in range(2)])
        # print(tabula.read_pdf(path, pages=[27], silent=True,columns=[163.88, 219.81, 289.27, 372.68, 397.36, 421.33, 445.27]))
        # print(tabula.read_pdf(path,pages=[22],silent=True,guess=False,columns=columncoordinate[:-1]))
        # print(tabula.read_pdf(path, pages=[23], silent=True,columns=columncoordinate[1:],output_path='temp'))
        # print(tabula.read_pdf(path, pages=[24], silent=True))
        # print(tabula.read_pdf(path, pages=[25], silent=True))
        # print(df)
        df.to_pickle('pickle'+path+'.pickle')
        # temp= pandas.read_pickle('pickle'+path+'.pickle')
        # print(path)
        # print(temp)
def tabulaLattice(pathList):
    create_project_dir("picklepdfFiles")


    for path in pathList:
        regex = re.compile(r"\d{4}")
        year = re.search(regex, path).group()
        if "Spring" in path:
            semester = "Spring"
        elif "Fall" in path:
            semester = "Fall"
        else:
            semester = "error"


        df = tabula.read_pdf(path,pages='all',silent=True,guess=True,lattice=True)
        df["Year"]=year
        df["Semester"]=semester
        print(df)
        df.to_csv('test/'+path+'.csv')
        df.to_pickle('pickle'+path+'.pickle')

def readFromPickle(pathList):
    result=[]
    for path in pathList:

        df= pandas.read_pickle('pickle'+path+'.pickle')
        # print(df)
        # print([column for column in df])
        df.columns=[column if column in ['Year', 'Semester'] else df[column].iloc[0] for column in df]
        # print(df[pandas.isnull(df['Section'])])
        df=df[pandas.notnull(df['Section'])]
        # print(df[df["Section"].str.isalpha()])
        df=df[df["Section"].str.isdigit()]
        # print(df[df["Section"].str.isdigit()])
        def fillNaNDepartmentSubjectCourse(columnName):
            DepartmentSubjectCourse=[]
            def fill(x):
                if type(x)==str:
                    # match = re.match(r"([a-zA-Z]+)(\d+[a-zA-Z]?)$",x,re.I)
                    # print(x)
                    x=' '.join(x.split())
                    x=' '.join(re.split(r"([a-zA-Z]+)(\d+[a-zA-Z]?$)",x)).strip()
                    # print(' '.join(re.split(r"([a-zA-Z]+)(\d+[a-zA-Z]?$)",x)).strip(),x)
                    # print(x)
                    DepartmentSubjectCourse.append(x)
                    return x
                else:
                    return DepartmentSubjectCourse[-1]
            df[columnName]=df[columnName].apply(fill)
            # print(DepartmentSubjectCourse)
            # print(df[columnName].apply(fill))

        def fixColumnHeader(df):
            flawedHeader=['Department', 'Subject', 'Course', 'Section', 'Instructor', 'A', 'B',
       'C', 'D DR', 'F', 'P', 'W', 'Grand Total', 'Year',
       'Semester']
            correctHeader=['Department', 'Subject', 'Course', 'Section', 'Instructor', 'A', 'B',
       'C', 'D', 'F', 'P', 'W', 'Total', 'Year',
       'Semester']
            

            def fixDDRcolumn(str):
                if type(str)==int:
                    return str
                list=str.split()
                return sum(int(x) for x in list)
            def fillnaWith0(str,df):

                # # print(column, str,'fillnaWith0')
                df[str] = df[str].fillna(0)
                # print(df)
                # # print(df[df[str].str.isalpha()])
                df[str] = df[str].apply(int)
                return df

            def fixHeaderSwitch(correctHeader,column,df):
                # print(df)
                # print(correctHeader,column)

                if column == 'D DR':
                    df[column] = df[column].fillna(0)
                    df[column] = df[column].apply(fixDDRcolumn)

                elif len(column) < 3:


                    df[column] = df[column].fillna(0)
                    df[column] = df[column].apply(int)
                    # df[column] = pandas.to_numeric(df[column])
                    # if (column == 'W'):
                    #     print(df[column])
                elif "Total" in column:
                    df[column] = df[column].apply(int)
                df = df.rename(columns={column: correctHeader})

                return df
            for column in df:
                if column in correctHeader:
                    # print('if')
                    df = fixHeaderSwitch(column, column, df)
                    # print(df)
                else:
                    # print('else')
                    for i in range(len(flawedHeader)):
                        if column in flawedHeader[i]:
                            df=fixHeaderSwitch(correctHeader[i],column,df)
                            break
                        elif(i==len(flawedHeader)-1):
                            # print(column)
                            # print(df.columns,column)
                            df.pop(column)
                            break
                            # df = df.drop(column)
            if "W" not in [column for column in df]:
                # df['test']=df[['A', 'B', 'C', 'D', 'F', 'P']].sum(axis=1)
                # print(df[["Total",'A', 'B', 'C', 'D', 'F', 'P']].diff(axis=1))
                # df=df.assign(W=lambda df:df["Total"]-df["A"]-df["B"]-df["C"]-df["D"]-df["F"]-df["P"])
                df['W']=df["Total"]-df["A"]-df["B"]-df["C"]-df["D"]-df["F"]-df["P"]




                # print(column,'column')
                # df=df.drop(column)

            return df




        fillNaNDepartmentSubjectCourse("Department")
        fillNaNDepartmentSubjectCourse("Subject")
        fillNaNDepartmentSubjectCourse("Course")
        # print(df)
        df=fixColumnHeader(df)
        # print(df.isnull().any())
        # print(df.head(),df.columns)
        # print(df)
        result.append(df)
        df.to_csv('test/'+path+'.csv')
    result=pandas.concat(result)
    # print(result[result.isnull().any(axis=1)])

    # print(result.isnull().any())
    # print(result)
    result.to_pickle('pickleResult.pickle')


def abcdpwtotal(fileList, projectName, outputFileName):
    df=pandas.read_pickle('pickleResult.pickle')
    df=df.fillna(0)
    print(df.isnull().values.any())
    # print(len(df))
    print(df.columns)
    dictionary={}
    for i in range(len(df)):
        key=df['Course'].iloc[i]+','+df['Instructor'].iloc[i]
        if key not in dictionary:
            dictionary[key] = [df['A'].iloc[i], df['B'].iloc[i], df['C'].iloc[i]
                , df['P'].iloc[i], df['D'].iloc[i], df['F'].iloc[i], df['W'].iloc[i], df['Total'].iloc[i]]

        else:
            temp=[df['A'].iloc[i], df['B'].iloc[i], df['C'].iloc[i]
                , df['P'].iloc[i], df['D'].iloc[i], df['F'].iloc[i], df['W'].iloc[i], df['Total'].iloc[i]]

            for index in range(len(dictionary[key])):
                dictionary[key][index] += temp[index]
        # print(type(dictionary[key]))
        # dictionary[key]=dictionary[key].astype(numpy.int32)

        for x in range(len(dictionary[key])):

            dictionary[key][x]=dictionary[key][x].item()
            # print(type(dictionary[key][x]))

    for key in dictionary:
        sum = 0
        for index in range(5):

            sum += dictionary[key][index]
            # print(dictionary[key][index],sum, dictionary[key][-1],dictionary[key][7],key)
            dictionary[key].append((ceil((sum / dictionary[key][7]) * 100)))
        for index in range(5,7):
            # print(dictionary[key][index],dictionary[key][-1],dictionary[key])
            dictionary[key].append((ceil((dictionary[key][index] / dictionary[key][7]) * 100)))
    path = get_path(projectName, outputFileName)
    # dataframe=pandas.DataFrame.from_dict(dictionary)
    # dataframe.to_json(path)

    with open(path, "w") as jsonFile:
        json.dump(dictionary, jsonFile)

    # print(dictionary)


# def getPicklePath():
#     return glob.glob('picklepdfFiles/*.pickle')
def pickleToCVS():

    df = pandas.read_pickle('pickleResult.pickle')
    print(df)
    for column in df:
        print(df[column].dtype)
        try:
            df = df.fillna[0]

        except Exception as e:
            print(e)
        try:
            df[column] = df[column].apply(str)
        except Exception as e:
            print("df[column] = df[column].apply(int)", e)
        for row in column:
            print(type(row),type('asdf'))
    df.to_csv('grade.csv')
def getPDFFilePath():
    return glob.glob('pdfFiles/*.pdf')

def getClassList():
    # classList=pandas.read_html("https://isiscc.smc.edu/pls/apex/f?p=123:1:10661265711409:pg_R_6372223720392943169:NO&pg_min_row=1&pg_max_rows=5000&pg_rows_fetched=5000#report")
    classList=pandas.read_html("https://isiscc.smc.edu/isisdoc/web_cat_sched_20171.html")

    # print(classList)

# getTableDataToPickle(getPDFFilePath()[1:])
# readFromPickle(getPDFFilePath()[:])
abcdpwtotal(CSV_GRADE_TABLES,PROJECT_NAME,GRADE_ALL_JSON)
# pickleToCVS()









# getTableDataToPickle(['pdfFiles/Fall 2016 - Grade Distribution.pdf'])
# tabulaLattice(['pdfFiles/Santa Monica College -Grade Distribution Fall 2017.pdf','pdfFiles/Santa Monica College -Grade Distribution Spring 2017.pdf'])
# readFromPickle(['pdfFiles/Spring 2016 Grade Distribution- Report.pdf'])
# readFromPickle(getPDFFilePath()[:])
