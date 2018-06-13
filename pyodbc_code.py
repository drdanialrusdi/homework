# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 08:52:10 2018

@author: 00130161
"""

import pyodbc
import pandas as pd
from datetime import datetime, date, timedelta

def extractbasedata(model_select,datadate):
    if model_select=='EFTB':
        service_id=109
    elif model_select=='EGTB':
        service_id=110
    elif model_select=='ELIB':
        service_id=111
    elif model_select=='EGIB':
        service_id=112
    elif model_select=='ELBB':
        service_id=114
    elif model_select=='EGBB':
        service_id=115
    
    if datadate.weekday()==5:
        pastdate=datadate-timedelta(days=7)
        pastdate=str(pastdate.year)+'-'+str(pastdate.month)+'-'+str(pastdate.day)
    else:
        pastdate=datadate-timedelta(days=1)
        pastdate=str(pastdate.year)+'-'+str(pastdate.month)+'-'+str(pastdate.day)
    
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=server_name;"
                      "Database=db_name;"
                      "Trusted_Connection=yes;")


    cursor = cnxn.cursor()
    cursor.execute('''SELECT  DATEPART(hour, CallStartDt)[Hour],
                    COUNT(SeqNum)[Offered_Call] 
                  FROM Detail.CallDetail
                  WHERE Service_ID=?
                  AND CallTypeId=1
                  AND CallCategoryId=1
                  AND BeginGaurdDt IS NOT NULL
                  AND CallStartDt =?
                  AND DATEPART(hour,CallStartDt) IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
                  GROUP BY DATEPART(hour, CallStartDt)''',service_id,pastdate)
    
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns=cursor.keys()
    for item in range(11):
        if not (df.Hour == item).any():
            df=df.append({'Hour':item,'Offered_Call':0},ignore_index=True)
    df=df.sort_values('Hour', ascending=False)
    return df['Offered_Call'].tolist()

def extracttodaydata(model_select,datadate):
    if model_select=='EFTB':
        service_id=109
    elif model_select=='EGTB':
        service_id=110
    elif model_select=='ELIB':
        service_id=111
    elif model_select=='EGIB':
        service_id=112
    elif model_select=='ELBB':
        service_id=114
    elif model_select=='EGBB':
        service_id=115
    
    #if datadate.weekday()==5:
    #    pastdate=datadate-timedelta(days=7)
    #    pastdate=str(pastdate.year)+'-'+str(pastdate.month)+'-'+str(pastdate.day)
    #else:
    #    pastdate=datadate-timedelta(days=1)
    #    pastdate=str(pastdate.year)+'-'+str(pastdate.month)+'-'+str(pastdate.day)
    pastdate=str(pastdate.year)+'-'+str(pastdate.month)+'-'+str(pastdate.day)
    
    
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=server_name;"
                      "Database=db_name;"
                      "Trusted_Connection=yes;")


    cursor = cnxn.cursor()
    cursor.execute('''SELECT  DATEPART(hour, CallStartDt)[Date],
                    COUNT(SeqNum)[Offered_Call] 
                  FROM Detail.CallDetail
                  WHERE Service_ID=?
                  AND CallTypeId=1
                  AND CallCategoryId=1
                  AND BeginGaurdDt IS NOT NULL
                  AND CallStartDt =?
                  AND DATEPART(hour,CallStartDt) IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
                  GROUP BY DATEPART(hour, CallStartDt)''',service_id,pastdate)
    
    
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns=cursor.keys()
    for item in range(11):
        if not (df.Hour == item).any():
            df=df.append({'Hour':item,'Offered_Call':0},ignore_index=True)
    df=df.sort_values('Hour', ascending=False)
    return df['Offered_Call'].tolist()