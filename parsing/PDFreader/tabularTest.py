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

def readFromPickle(pathList):
    for path in pathList:

        temp= pandas.read_pickle('pickle'+path+'.pickle')
        print(path)
        print(temp)



    # tabula.convert_into("pdfFiles/selection.pdf", "output.json", output_format="json")
    # for i in df:
    #     print(i)
    # print(df)

# def getPicklePath():
#     return glob.glob('picklepdfFiles/*.pickle')

def getPDFFilePath():
    return glob.glob('pdfFiles/*.pdf')

def getClassList():
    # classList=pandas.read_html("https://isiscc.smc.edu/pls/apex/f?p=123:1:10661265711409:pg_R_6372223720392943169:NO&pg_min_row=1&pg_max_rows=5000&pg_rows_fetched=5000#report")
    classList=pandas.read_html("https://isiscc.smc.edu/isisdoc/web_cat_sched_20171.html")

    print(classList)

# getTableDataToPickle(getPDFFilePath()[1:])
# readFromPickle(getPDFFilePath())