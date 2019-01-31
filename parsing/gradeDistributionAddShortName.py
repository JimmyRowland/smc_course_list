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


def addProfessorshortName():
    df = pandas.read_pickle('pickleResult.pickle')
    df_new=0
    # print(df)
    df['shortName']=df['Instructor'].str.split(' ').str.get(0)+' '+df['Instructor'].str.split(' ').str.get(-1)
    df['lastAndMiddleName']=df['Instructor'].str.split(' ').str.get(0)+' '+df['Instructor'].str.split(' ').str.get(1)
    df['longName'] = '0'
    namelist=[]
    for index, row in df.iterrows():
        # print(row['shortName'])
        # print(namelist)
        if row['shortName'] not in namelist:
            # print(row['shortName'])
            df_temp=df[df['shortName']==row['shortName']]
            # print(df[df['shortName']==row['shortName']])
            # df=df[df['shortName']!=row['shortName']]
            # print(df)
            # print('+++++++++++')
            # print(df_temp)
            df_temp['lenLongName']=df_temp['Instructor'].str.len()

            # print(df_temp['lenLongName'])
            # print(df_temp.loc[df_temp['lenLongName'].idxmax()]['Instructor'])
            longNameDf=df_temp.loc[df_temp['lenLongName'].idxmax()]
            shortNameDf = df_temp.loc[df_temp['lenLongName'].idxmin()]
            # print(longNameDf)
            # print(type(longNameDf['Instructor']))
            if type(longNameDf['Instructor'])==str:
                # print(type(longNameDf['Instructor']))
                longName=longNameDf['Instructor']
            else:
                longName = longNameDf['Instructor'].iloc[0]
            if type(shortNameDf['Instructor'])==str:
                shortName=shortNameDf['Instructor']
            else:
                shortName = shortNameDf['Instructor'].iloc[0]
            if longName!=shortName:
                print('Longest name: {}, shortest Name: {}, Last Name and First Name Initial: {}'.format(longName, shortName,row["shortName"]) )
            # print(df_temp['lenLongName'].max())
            # print(longName)

            # df_temp['longName'] = longName
            df.ix[df['shortName']==row['shortName'],'longName']=longName
            # print(df_temp)
            # print("-----------------")
            # print(df)
            namelist.append(row['shortName'])



            if(row['lastAndMiddleName']!=row['shortName']):
                df_temp = df[df['lastAndMiddleName'] == row['lastAndMiddleName']]
                if(df_temp.empty):

                    print("professor with only firstname",df_temp,row['lastAndMiddleName'],row['shortName'],row)

                else:
                    df_temp['lenLongName'] = df_temp['Instructor'].str.len()

                    longNameDf = df_temp.loc[df_temp['lenLongName'].idxmax()]
                    shortNameDf = df_temp.loc[df_temp['lenLongName'].idxmin()]
                    if type(longNameDf['Instructor']) == str:
                        # print(type(longNameDf['Instructor']))
                        longName = longNameDf['Instructor']
                    else:
                        longName = longNameDf['Instructor'].iloc[0]
                    if type(shortNameDf['Instructor']) == str:
                        shortName = shortNameDf['Instructor']
                    else:
                        shortName = shortNameDf['Instructor'].iloc[0]
                    if longName != shortName:
                        print('Longest name: {}, shortest Name: {}, Last Name and Middle Name: {}'.format(longName,
                                                                                                                 shortName, row[
                                                                                                                     "shortName"]))
                    # print(df_temp['lenLongName'].max())
                    # print(longName)

                    # df_temp['longName'] = longName


                    df.ix[df['lastAndMiddleName'] == row['lastAndMiddleName'], 'longName'] = longName
                    # print(df_temp)
                    # print("-----------------")
                    # print(df)
                    namelist.append(row['lastAndMiddleName'])

    print(df)
    df.to_csv("withLongName.csv")





# addProfessorshortName()








