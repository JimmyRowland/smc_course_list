import sys
import pdfquery
from pdfquery.cache import FileCache
from utils import BaseTestCase
import re
import inspect

# from .utils import BaseTestCase


class PDFqueryGrade(BaseTestCase):


    @classmethod
    def setUpClass(cls):
        cls.pdf = pdfquery.PDFQuery("pdfFiles/Fall 2015 Grade Distribution- Report.pdf", parse_tree_cacher=FileCache("/tmp/"))
        cls.pdf.load(0)
        # cls.pdf.tree.write("test2.xml", pretty_print=True, encoding="utf-8")

    def getSemesterAndYear(self):
        lable=self.pdf.pq('LTTextLineHorizontal:contains("Santa Monica College")').text()
        regex=re.compile(r"\d{4}")
        year=re.search(regex,lable).group()
        if "Spring" in lable:
            semester="Spring"
        elif "Fall" in lable:
            semester="Fall"
        else:
            semester="error"
        print(year,semester)

    # @staticmethod
    def getCenter(self, bbox):
        x = (float(bbox.attr("x0")) + float(bbox.attr("x1"))) / 2
        y = (float(bbox.attr("y0")) + float(bbox.attr("y1"))) / 2
        return [x, y]

    def extractData(self):

        def gradeLetterPositionFilter():
            return float(this.get('x0', 0)) > instructorCenter[0]
            # print (dir(this))
            # print(this.attrib)

            # return this.get('text', 0) < 3

        pageWidth = self.pdf.pq('LTPage').attr("x1")
        # print(width)
        department = self.pdf.pq('LTTextLineHorizontal:contains("Department")')
        departmentCenter = self.getCenter(department)
        gridHeight=department.attr('height')
        # print("%s,%s,%s,%s" % (float(width)-100,0, width, departmentCenter[1] + 0.1))
        firstRow=self.pdf.pq('LTTextLineHorizontal:overlaps_bbox("0,%s,%s,%s")' % (departmentCenter[1],pageWidth,departmentCenter[1]+0.1))
        secondRow=self.pdf.pq('LTTextLineHorizontal:overlaps_bbox("0,%s,%s,%s")' % (departmentCenter[1]-21.6,pageWidth,departmentCenter[1]-21.5))
        x0FirstRow=[float(i.attr('x0')) for i in firstRow.items()]
        firstRowText=[firstRow.eq(i) for i in range(len(firstRow)) ]
        firstRowText.sort(key= lambda x: float(x.attr('x0')))
        # print(firstRow.items()[0])
        print(firstRowText[0].text())
        x0FirstRow.sort()

        print(dir(firstRow))
        # print(inspect.getsource(firstRow[0].text))
        print(inspect.getsource(firstRow.text))
        print(inspect.getmembers(firstRow))
        print('children',firstRow.children())
        print(firstRow.eq(0))
        print(firstRow.find('P'))
        print(firstRow.eq(4).text())

        print(x0FirstRow)
        # print(firstRow[0].get_text())
        print(firstRow.text())
        print(secondRow.text())
        print(secondRow.eq(11).text())


        subject = self.pdf.pq('LTTextLineHorizontal:contains("Subject")')
        course = self.pdf.pq('LTTextLineHorizontal:contains("Course")')
        section = self.pdf.pq('LTTextLineHorizontal:contains("Section")')
        instructor = self.pdf.pq('LTTextLineHorizontal:contains("Instructor")')


        instructorCenter = self.getCenter(instructor)

        gradeA = self.pdf.pq('LTTextLineHorizontal:contains("A")').filter(gradeLetterPositionFilter)
        gradeB = self.pdf.pq('LTTextLineHorizontal:contains("B")').filter(gradeLetterPositionFilter)
        gradeC = self.pdf.pq('LTTextLineHorizontal:contains("C")').filter(gradeLetterPositionFilter)
        gradeD = self.pdf.pq('LTTextLineHorizontal:contains("D")').filter(gradeLetterPositionFilter)
        gradeF = self.pdf.pq('LTTextLineHorizontal:contains("F")').filter(gradeLetterPositionFilter)
        gradeP = self.pdf.pq('LTTextLineHorizontal:contains("P")').filter(gradeLetterPositionFilter)
        print(department)
        print(gradeP)

        # text=[]
        # def add_text(tag, no_tail=False):
        #     if tag.text and not isinstance(tag, lxml.etree._Comment):
        #         text.append(tag.text)
        #     for child in tag.getchildren():
        #         add_text(child)
        #     if not no_tail and tag.tail:
        #         text.append(tag.tail)
        # for i in gradeP:
        #     add_text(i, no_tail=True)
        #     print(text)
        #
        #     print(dir(i))
        #     print(i.text,i.tail)



            # if len(i.text())<3:
            #     gradeP=i
            #     break
        gradeW = self.pdf.pq('LTTextLineHorizontal:contains("W")').filter(gradeLetterPositionFilter)
        total = self.pdf.pq('LTTextLineHorizontal:contains("Total")')
        firstDepartmentName=self.pdf.pq('LTTextLineHorizontal:contains("Art")')

        firstDepartmentNameCenter=self.getCenter(firstDepartmentName)
        gridHeight=(departmentCenter[1]+firstDepartmentNameCenter[1])/2
        # print(inspect.getsource(gradeP.text))
        print(gradeA.text(),gradeC.text(),gradeB.text(),gradeP.text())
        # print(gradeB.text())



    # pdf.tree.write("test2.xml", pretty_print=True, encoding="utf-8")
test= PDFqueryGrade()
test.setUpClass()
# test.getSemester()
test.extractData()



# temp=[545.59,524.022,502.217,436.762,414.957,393.182]
# for i in range(5):
#     print(temp[i]-temp[i+1])