# -*- coding: utf-8 -*-
"""
Created on Mon May 28 12:04:43 2018

@author: 00130161
"""

from keras.models import load_model
from sklearn.externals import joblib
import numpy as np
from datetime import datetime


def currentday():
    day=datetime.now().weekday()
    return day

def currenttime():
    timenow=datetime.now().hour
    if timenow < 8:
        timenow=8
    elif timenow>18:
        timenow=18
    return timenow

timearray=np.eye(11)
dayarray=np.eye(5)


def oc_model(model_select='EFTB',working_day=True):
    if model_select.upper()=='EFTB':
        if working_day==True:
            model=load_model('keras_model\\EFTBOffered_Call_workingdaymodel.hdf5')
        elif working_day==False:
            model=load_model('keras_model\\EFTBOffered_Call_saturdaymodel.hdf5')
    if model_select.upper()=='EGTB':
        if working_day==True:
            model=load_model('keras_model\\EGTBOffered_Call_workingdaymodel.hdf5')
        elif working_day==False:
            model=load_model('keras_model\\EGTBOffered_Call_saturdaymodel.hdf5')
    if model_select.upper()=='EGIB':
        if working_day==True:
            model=load_model('keras_model\\EGIBOffered_Call_workingdaymodel.hdf5')
        elif working_day==False:
            model=load_model('keras_model\\EGIBOffered_Call_saturdaymodel.hdf5')
    if model_select.upper()=='ELIB':
        if working_day==True:
            model=load_model('keras_model\\ELIBOffered_Call_workingdaymodel.hdf5')
        elif working_day==False:
            model=load_model('keras_model\\ELIBOffered_Call_saturdaymodel.hdf5')
    if model_select.upper()=='ELBB':
        if working_day==True:
            model=load_model('keras_model\\ELBBOffered_Call_workingdaymodel.hdf5')
    if model_select.upper()=='EGBB':
        if working_day==True:
            model=load_model('keras_model\\EGBBOffered_Call_workingdaymodel.hdf5')

    return model

def scaler_model(model_select='EFTB', working_day=True):
    if model_select.upper()=='EFTB':
        if working_day==True:
            model=joblib.load('keras_model\\EFTBScalerworkingday.pkl')
        if working_day==False:
            model=joblib.load('keras_model\\EFTBScalersaturday.pkl')
    if model_select.upper()=='EGTB':
        if working_day==True:
            model=joblib.load('keras_model\\EGTBScalerworkingday.pkl')
        if working_day==False:
            model=joblib.load('keras_model\\EGTBScalersaturday.pkl')
    if model_select.upper()=='EGIB':
        if working_day==True:
            model=joblib.load('keras_model\\EGIBScalerworkingday.pkl')
        if working_day==False:
            model=joblib.load('keras_model\\EGIBScalersaturday.pkl')
    if model_select.upper()=='ELIB':
        if working_day==True:
            model=joblib.load('keras_model\\ELIBScalerworkingday.pkl')
        if working_day==False:
            model=joblib.load('keras_model\\ELIBScalersaturday.pkl')
    if model_select.upper()=='ELBB':
        if working_day==True:
            model=joblib.load('keras_model\\ELBBScalerworkingday.pkl')
    if model_select.upper()=='EGBB':
        if working_day==True:
            model=joblib.load('keras_model\\EGBBScalerworkingday.pkl')

    return model

def oc_predict(X, model_select='EFTB', working_day=True):
    """
    X = list or array in shape (1,27,1) or (1,10,1) or (1,27) or (1,10)
    model_select = type of model to use for prediction based on skill
    working_day = if False, then it refer for Saturday
    return one step ahead prediction
    """    
    if isinstance(X,list):
        X=np.array(X)
    if len(X.shape)==2:
        X=X.reshape(X.shape[0],X.shape[1],1)
    elif len(X.shape)!=3:
        raise
    if working_day==True:
        assert(X.shape[1]==27)
    elif working_day==False:
        assert(X.shape[1]==10)
    model=oc_model(model_select=model_select,working_day=working_day)
    scale=scaler_model(model_select=model_select,working_day=working_day)
    
    X=X.reshape(X.shape[0],27)
    datafirst=X[:,:11]
    datasecond=X[:,11:]
    datafirst=scale.transform(datafirst)
    X=np.concatenate([datafirst,datasecond],axis=1)
    X=X.reshape(X.shape[0],X.shape[1],1)
    
    scalar_Y=model.predict(X)
    pred=scale.inverse_transform(scalar_Y)
    pred=np.squeeze(pred)
    
    return pred

#Edit the current time so it can consider loop
def oc_predict_simulation(data,new_data=[],model_select='EFTB'):
    '''
    data=array of t-1 until t-11 which shape (1,11) or (11,) of the day before
    new_data=new data that coming in
    '''
    if isinstance(data,list):
        data=np.array(data)
        data=data.reshape(1,len(data))
        
    working_day=bool(currentday()!=5 | currentday()!=6)
    if working_day==True:
        '''
        Change back currentday to the formula
        '''
        today=dayarray[0,:]
        #today=dayarray[currentday(),:]
        fullhour=19
    else:
        today=[]
        fullhour=13
    Pred_memory=[]
    Full_prediction=[]
    
    #Repeat 11 times for 
    for pred in range(11):
        data2=data[0,:11-pred]
        
        if len(Pred_memory)!=0:
            #insert prediction infront of data2
            data2=np.insert(data2,0,Pred_memory)
        data2=data2.reshape(1,len(data2))
        data_to_predict=np.concatenate((data2,[today],timearray[pred,:].reshape(1,11)),axis=1)
        print(data_to_predict)
        print('*'*30)
        Full_prediction.append(data_to_predict)
        prediction=oc_predict(data_to_predict,model_select=model_select,working_day=working_day)
        Pred_memory=np.insert(Pred_memory,0,prediction)
    Full_prediction=np.concatenate(Full_prediction)
    
    if len(new_data)==0:
        pred=oc_predict(Full_prediction,model_select=model_select,working_day=working_day)
    else:
        predfull=oc_predict(Full_prediction,model_select=model_select,working_day=working_day)
        for i,item in enumerate(new_data):
            for j in range(11):
                try:
                    Full_prediction[i+j+1,j]=item
                except:
                    continue
        pred=oc_predict(Full_prediction,model_select=model_select,working_day=working_day)
        pred=np.concatenate((predfull[:len(new_data)],pred[len(new_data):]))
    return pred

def headcount_suggestion(pred,models):
    headcount=[]
    for item in pred:
        if item!='NaN':    
            if item<=10:
                headcount.append(models['10 Call'])
            elif item<=20:
                headcount.append(models['20 Call'])
            elif item<=30:
                headcount.append(models['30 Call'])
            elif item<=40:
                headcount.append(models['40 Call'])
            elif item<=50:
                headcount.append(models['50 Call'])
            elif item<=60:
                headcount.append(models['60 Call'])
            elif item<=70:
                headcount.append(models['70 Call'])
            elif item<=80:
                headcount.append(models['80 Call'])
            elif item<=90:
                headcount.append(models['90 Call'])
            elif item<=100:
                headcount.append(models['100 Call'])
            elif item<=110:
                headcount.append(models['110 Call'])
            elif item<=120:
                headcount.append(models['120 Call'])
            elif item<=130:
                headcount.append(models['130 Call'])
            elif item<=140:
                headcount.append(models['140 Call'])
            else:
                headcount.append(models['150 Call'])
        elif item=='NaN':
            headcount.append(list(np.zeros(24)))
    return headcount

def oc_dict(data, models, new_data=[],model_select='EFTB'):
    
    pred=oc_predict_simulation(data,new_data=new_data,model_select=model_select)
    data={}
    new_data2=new_data.copy()
    if len(pred)==5:
        pred.extend(['NaN']*6)
    new_data2.extend(['NaN']*(11-len(new_data)))
    data['title']=model_select
    data['lapanpagip']=pred[0]
    data['lapanpagia']=new_data2[0]
    data['sembilanpagip']=pred[1]
    data['sembilanpagia']=new_data2[1]
    data['sepuluhpagip']=pred[2]
    data['sepuluhpagia']=new_data2[2]
    data['sebelaspagip']=pred[3]
    data['sebelaspagia']=new_data2[3]
    data['duabelasptgp']=pred[4]
    data['duabelasptga']=new_data2[4]
    data['satuptgp']=pred[5]
    data['satuptga']=new_data2[5]
    data['duaptgp']=pred[6]
    data['duaptga']=new_data2[6]
    data['tigaptgp']=pred[7]
    data['tigaptga']=new_data2[7]
    data['empatptgp']=pred[8]
    data['empatptga']=new_data2[8]
    data['limaptgp']=pred[9]
    data['limaptga']=new_data2[9]
    data['enamptgp']=pred[10]
    data['enamptga']=new_data2[10]
    
    headcount=headcount_suggestion(pred, models)
    
    #pukul 8,until 18
    data['one']=[headcount[0][0],headcount[1][0],headcount[2][0],headcount[3][0],headcount[4][0],headcount[5][0],headcount[6][0],headcount[7][0],headcount[8][0],headcount[9][0],headcount[10][0]]
    data['two']=[headcount[0][1],headcount[1][1],headcount[2][1],headcount[3][1],headcount[4][1],headcount[5][1],headcount[6][1],headcount[7][1],headcount[8][1],headcount[9][1],headcount[10][1]]
    data['three']=[headcount[0][2],headcount[1][2],headcount[2][2],headcount[3][2],headcount[4][2],headcount[5][2],headcount[6][2],headcount[7][2],headcount[8][2],headcount[9][2],headcount[10][2]]
    data['four']=[headcount[0][3],headcount[1][3],headcount[2][3],headcount[3][3],headcount[4][3],headcount[5][3],headcount[6][3],headcount[7][3],headcount[8][3],headcount[9][3],headcount[10][3]]
    data['five']=[headcount[0][4],headcount[1][4],headcount[2][4],headcount[3][4],headcount[4][4],headcount[5][4],headcount[6][4],headcount[7][4],headcount[8][4],headcount[9][4],headcount[10][4]]
    data['six']=[headcount[0][5],headcount[1][5],headcount[2][5],headcount[3][5],headcount[4][5],headcount[5][5],headcount[6][5],headcount[7][5],headcount[8][5],headcount[9][5],headcount[10][5]]
    data['seven']=[headcount[0][6],headcount[1][6],headcount[2][6],headcount[3][6],headcount[4][6],headcount[5][6],headcount[6][6],headcount[7][6],headcount[8][6],headcount[9][6],headcount[10][6]]
    data['eight']=[headcount[0][7],headcount[1][7],headcount[2][7],headcount[3][7],headcount[4][7],headcount[5][7],headcount[6][7],headcount[7][7],headcount[8][7],headcount[9][7],headcount[10][7]]
    data['nine']=[headcount[0][8],headcount[1][8],headcount[2][8],headcount[3][8],headcount[4][8],headcount[5][8],headcount[6][8],headcount[7][8],headcount[8][8],headcount[9][8],headcount[10][8]]
    data['ten']=[headcount[0][9],headcount[1][9],headcount[2][9],headcount[3][9],headcount[4][9],headcount[5][9],headcount[6][9],headcount[7][9],headcount[8][9],headcount[9][9],headcount[10][9]]
    data['eleven']=[headcount[0][10],headcount[1][10],headcount[2][10],headcount[3][10],headcount[4][10],headcount[5][10],headcount[6][10],headcount[7][10],headcount[8][10],headcount[9][10],headcount[10][10]]
    data['twelve']=[headcount[0][11],headcount[1][11],headcount[2][11],headcount[3][11],headcount[4][11],headcount[5][11],headcount[6][11],headcount[7][11],headcount[8][11],headcount[9][11],headcount[10][11]]
    data['thirteen']=[headcount[0][12],headcount[1][12],headcount[2][12],headcount[3][12],headcount[4][12],headcount[5][12],headcount[6][12],headcount[7][12],headcount[8][12],headcount[9][12],headcount[10][12]]
    data['fourteen']=[headcount[0][13],headcount[1][13],headcount[2][13],headcount[3][13],headcount[4][13],headcount[5][13],headcount[6][13],headcount[7][13],headcount[8][13],headcount[9][13],headcount[10][13]]
    data['fifthteen']=[headcount[0][14],headcount[1][14],headcount[2][14],headcount[3][14],headcount[4][14],headcount[5][14],headcount[6][14],headcount[7][14],headcount[8][14],headcount[9][14],headcount[10][14]]
    data['sixteen']=[headcount[0][15],headcount[1][15],headcount[2][15],headcount[3][15],headcount[4][15],headcount[5][15],headcount[6][15],headcount[7][15],headcount[8][15],headcount[9][15],headcount[10][15]]
    data['seventeen']=[headcount[0][16],headcount[1][16],headcount[2][16],headcount[3][16],headcount[4][16],headcount[5][16],headcount[6][16],headcount[7][16],headcount[8][16],headcount[9][16],headcount[10][16]]
    data['eighteen']=[headcount[0][17],headcount[1][17],headcount[2][17],headcount[3][17],headcount[4][17],headcount[5][17],headcount[6][17],headcount[7][17],headcount[8][17],headcount[9][17],headcount[10][17]]
    data['nineteen']=[headcount[0][18],headcount[1][18],headcount[2][18],headcount[3][18],headcount[4][18],headcount[5][18],headcount[6][18],headcount[7][18],headcount[8][18],headcount[9][18],headcount[10][18]]
    data['twenty']=[headcount[0][19],headcount[1][19],headcount[2][19],headcount[3][19],headcount[4][19],headcount[5][19],headcount[6][19],headcount[7][19],headcount[8][19],headcount[9][19],headcount[10][19]]
    data['twentyone']=[headcount[0][20],headcount[1][20],headcount[2][20],headcount[3][20],headcount[4][20],headcount[5][20],headcount[6][20],headcount[7][20],headcount[8][20],headcount[9][20],headcount[10][20]]
    data['twentytwo']=[headcount[0][21],headcount[1][21],headcount[2][21],headcount[3][21],headcount[4][21],headcount[5][21],headcount[6][21],headcount[7][21],headcount[8][21],headcount[9][21],headcount[10][21]]
    data['twentythree']=[headcount[0][22],headcount[1][22],headcount[2][22],headcount[3][22],headcount[4][22],headcount[5][22],headcount[6][22],headcount[7][22],headcount[8][22],headcount[9][22],headcount[10][22]]
    data['twentyfour']=[headcount[0][23],headcount[1][23],headcount[2][23],headcount[3][23],headcount[4][23],headcount[5][23],headcount[6][23],headcount[7][23],headcount[8][23],headcount[9][23],headcount[10][23]]
    
    return data

def headcount_suggestion_all(pred,models):
    headcount=[]
    for item in pred:
        if item!='NaN':    
            if item<=10:
                headcount.append(models['10 Call'])
            elif item<=20:
                headcount.append(models['20 Call'])
            elif item<=30:
                headcount.append(models['30 Call'])
            elif item<=40:
                headcount.append(models['40 Call'])
            elif item<=50:
                headcount.append(models['50 Call'])
            elif item<=60:
                headcount.append(models['60 Call'])
            elif item<=70:
                headcount.append(models['70 Call'])
            elif item<=80:
                headcount.append(models['80 Call'])
            elif item<=90:
                headcount.append(models['90 Call'])
            elif item<=100:
                headcount.append(models['100 Call'])
            elif item<=110:
                headcount.append(models['110 Call'])
            elif item<=120:
                headcount.append(models['120 Call'])
            elif item<=130:
                headcount.append(models['130 Call'])
            elif item<=140:
                headcount.append(models['140 Call'])
            elif item<=150:
                headcount.append(models['150 Call'])
            elif item<=160:
                headcount.append(models['160 Call'])
            elif item<=170:
                headcount.append(models['170 Call'])
            elif item<=180:
                headcount.append(models['180 Call'])
            elif item<=190:
                headcount.append(models['190 Call'])
            elif item<=200:
                headcount.append(models['200 Call'])
            elif item<=210:
                headcount.append(models['210 Call'])
            elif item<=220:
                headcount.append(models['220 Call'])
            elif item<=230:
                headcount.append(models['230 Call'])
            elif item<=240:
                headcount.append(models['240 Call'])
            elif item<=250:
                headcount.append(models['250 Call'])
            elif item<=260:
                headcount.append(models['260 Call'])
            elif item<=270:
                headcount.append(models['270 Call'])
            elif item<=280:
                headcount.append(models['280 Call'])
            elif item<=290:
                headcount.append(models['290 Call'])
            elif item<=300:
                headcount.append(models['300 Call'])
            elif item<=310:
                headcount.append(models['310 Call'])
            elif item<=320:
                headcount.append(models['320 Call'])
            elif item<=330:
                headcount.append(models['330 Call'])
            elif item<=340:
                headcount.append(models['340 Call'])
            elif item<=350:
                headcount.append(models['350 Call'])
            elif item<=360:
                headcount.append(models['360 Call'])
            elif item<=370:
                headcount.append(models['370 Call'])
            elif item<=380:
                headcount.append(models['380 Call'])
            elif item<=390:
                headcount.append(models['390 Call'])
            elif item<=400:
                headcount.append(models['400 Call'])
            elif item<=410:
                headcount.append(models['410 Call'])
            elif item<=420:
                headcount.append(models['420 Call'])
            elif item<=430:
                headcount.append(models['430 Call'])
            elif item<=440:
                headcount.append(models['440 Call'])
            elif item<=450:
                headcount.append(models['450 Call'])
            elif item<=460:
                headcount.append(models['460 Call'])
            elif item<=470:
                headcount.append(models['470 Call'])
            elif item<=480:
                headcount.append(models['480 Call'])
            elif item<=490:
                headcount.append(models['490 Call'])
            else:
                headcount.append(models['500 Call'])
        elif item=='NaN':
            headcount.append(list(np.zeros(24)))
    return headcount

def oc_dict_all(pred, models, new_data=[]):
    data={}
    data['lapanpagip']=pred[0]
    data['lapanpagia']=new_data[0]
    data['sembilanpagip']=pred[1]
    data['sembilanpagia']=new_data[1]
    data['sepuluhpagip']=pred[2]
    data['sepuluhpagia']=new_data[2]
    data['sebelaspagip']=pred[3]
    data['sebelaspagia']=new_data[3]
    data['duabelasptgp']=pred[4]
    data['duabelasptga']=new_data[4]
    data['satuptgp']=pred[5]
    data['satuptga']=new_data[5]
    data['duaptgp']=pred[6]
    data['duaptga']=new_data[6]
    data['tigaptgp']=pred[7]
    data['tigaptga']=new_data[7]
    data['empatptgp']=pred[8]
    data['empatptga']=new_data[8]
    data['limaptgp']=pred[9]
    data['limaptga']=new_data[9]
    data['enamptgp']=pred[10]
    data['enamptga']=new_data[10]
    
    headcount=headcount_suggestion_all(pred, models)

    data['one']=[headcount[0][0],headcount[1][0],headcount[2][0],headcount[3][0],headcount[4][0],headcount[5][0],headcount[6][0],headcount[7][0],headcount[8][0],headcount[9][0],headcount[10][0]]
    data['two']=[headcount[0][1],headcount[1][1],headcount[2][1],headcount[3][1],headcount[4][1],headcount[5][1],headcount[6][1],headcount[7][1],headcount[8][1],headcount[9][1],headcount[10][1]]
    data['three']=[headcount[0][2],headcount[1][2],headcount[2][2],headcount[3][2],headcount[4][2],headcount[5][2],headcount[6][2],headcount[7][2],headcount[8][2],headcount[9][2],headcount[10][2]]
    data['four']=[headcount[0][3],headcount[1][3],headcount[2][3],headcount[3][3],headcount[4][3],headcount[5][3],headcount[6][3],headcount[7][3],headcount[8][3],headcount[9][3],headcount[10][3]]
    data['five']=[headcount[0][4],headcount[1][4],headcount[2][4],headcount[3][4],headcount[4][4],headcount[5][4],headcount[6][4],headcount[7][4],headcount[8][4],headcount[9][4],headcount[10][4]]
    data['six']=[headcount[0][5],headcount[1][5],headcount[2][5],headcount[3][5],headcount[4][5],headcount[5][5],headcount[6][5],headcount[7][5],headcount[8][5],headcount[9][5],headcount[10][5]]
    data['seven']=[headcount[0][6],headcount[1][6],headcount[2][6],headcount[3][6],headcount[4][6],headcount[5][6],headcount[6][6],headcount[7][6],headcount[8][6],headcount[9][6],headcount[10][6]]
    data['eight']=[headcount[0][7],headcount[1][7],headcount[2][7],headcount[3][7],headcount[4][7],headcount[5][7],headcount[6][7],headcount[7][7],headcount[8][7],headcount[9][7],headcount[10][7]]
    data['nine']=[headcount[0][8],headcount[1][8],headcount[2][8],headcount[3][8],headcount[4][8],headcount[5][8],headcount[6][8],headcount[7][8],headcount[8][8],headcount[9][8],headcount[10][8]]
    data['ten']=[headcount[0][9],headcount[1][9],headcount[2][9],headcount[3][9],headcount[4][9],headcount[5][9],headcount[6][9],headcount[7][9],headcount[8][9],headcount[9][9],headcount[10][9]]
    data['eleven']=[headcount[0][10],headcount[1][10],headcount[2][10],headcount[3][10],headcount[4][10],headcount[5][10],headcount[6][10],headcount[7][10],headcount[8][10],headcount[9][10],headcount[10][10]]
    data['twelve']=[headcount[0][11],headcount[1][11],headcount[2][11],headcount[3][11],headcount[4][11],headcount[5][11],headcount[6][11],headcount[7][11],headcount[8][11],headcount[9][11],headcount[10][11]]
    data['thirteen']=[headcount[0][12],headcount[1][12],headcount[2][12],headcount[3][12],headcount[4][12],headcount[5][12],headcount[6][12],headcount[7][12],headcount[8][12],headcount[9][12],headcount[10][12]]
    data['fourteen']=[headcount[0][13],headcount[1][13],headcount[2][13],headcount[3][13],headcount[4][13],headcount[5][13],headcount[6][13],headcount[7][13],headcount[8][13],headcount[9][13],headcount[10][13]]
    data['fifthteen']=[headcount[0][14],headcount[1][14],headcount[2][14],headcount[3][14],headcount[4][14],headcount[5][14],headcount[6][14],headcount[7][14],headcount[8][14],headcount[9][14],headcount[10][14]]
    data['sixteen']=[headcount[0][15],headcount[1][15],headcount[2][15],headcount[3][15],headcount[4][15],headcount[5][15],headcount[6][15],headcount[7][15],headcount[8][15],headcount[9][15],headcount[10][15]]
    data['seventeen']=[headcount[0][16],headcount[1][16],headcount[2][16],headcount[3][16],headcount[4][16],headcount[5][16],headcount[6][16],headcount[7][16],headcount[8][16],headcount[9][16],headcount[10][16]]
    data['eighteen']=[headcount[0][17],headcount[1][17],headcount[2][17],headcount[3][17],headcount[4][17],headcount[5][17],headcount[6][17],headcount[7][17],headcount[8][17],headcount[9][17],headcount[10][17]]
    data['nineteen']=[headcount[0][18],headcount[1][18],headcount[2][18],headcount[3][18],headcount[4][18],headcount[5][18],headcount[6][18],headcount[7][18],headcount[8][18],headcount[9][18],headcount[10][18]]
    data['twenty']=[headcount[0][19],headcount[1][19],headcount[2][19],headcount[3][19],headcount[4][19],headcount[5][19],headcount[6][19],headcount[7][19],headcount[8][19],headcount[9][19],headcount[10][19]]
    data['twentyone']=[headcount[0][20],headcount[1][20],headcount[2][20],headcount[3][20],headcount[4][20],headcount[5][20],headcount[6][20],headcount[7][20],headcount[8][20],headcount[9][20],headcount[10][20]]
    data['twentytwo']=[headcount[0][21],headcount[1][21],headcount[2][21],headcount[3][21],headcount[4][21],headcount[5][21],headcount[6][21],headcount[7][21],headcount[8][21],headcount[9][21],headcount[10][21]]
    data['twentythree']=[headcount[0][22],headcount[1][22],headcount[2][22],headcount[3][22],headcount[4][22],headcount[5][22],headcount[6][22],headcount[7][22],headcount[8][22],headcount[9][22],headcount[10][22]]
    data['twentyfour']=[headcount[0][23],headcount[1][23],headcount[2][23],headcount[3][23],headcount[4][23],headcount[5][23],headcount[6][23],headcount[7][23],headcount[8][23],headcount[9][23],headcount[10][23]]
    data['twentyfive']=[headcount[0][24],headcount[1][24],headcount[2][24],headcount[3][24],headcount[4][24],headcount[5][24],headcount[6][24],headcount[7][24],headcount[8][24],headcount[9][24],headcount[10][24]]
    data['twentysix']=[headcount[0][25],headcount[1][25],headcount[2][25],headcount[3][25],headcount[4][25],headcount[5][25],headcount[6][25],headcount[7][25],headcount[8][25],headcount[9][25],headcount[10][25]]
    data['twentyseven']=[headcount[0][26],headcount[1][26],headcount[2][26],headcount[3][26],headcount[4][26],headcount[5][26],headcount[6][26],headcount[7][26],headcount[8][26],headcount[9][26],headcount[10][26]]
    data['twentyeight']=[headcount[0][27],headcount[1][27],headcount[2][27],headcount[3][27],headcount[4][27],headcount[5][27],headcount[6][27],headcount[7][27],headcount[8][27],headcount[9][27],headcount[10][27]]
    data['twentynine']=[headcount[0][28],headcount[1][28],headcount[2][28],headcount[3][28],headcount[4][28],headcount[5][28],headcount[6][28],headcount[7][28],headcount[8][28],headcount[9][28],headcount[10][28]]
    data['thirty']=[headcount[0][29],headcount[1][29],headcount[2][29],headcount[3][29],headcount[4][29],headcount[5][29],headcount[6][29],headcount[7][29],headcount[8][29],headcount[9][29],headcount[10][29]]
    data['thirtyone']=[headcount[0][30],headcount[1][30],headcount[2][30],headcount[3][30],headcount[4][30],headcount[5][30],headcount[6][30],headcount[7][30],headcount[8][30],headcount[9][30],headcount[10][30]]
    data['thirtytwo']=[headcount[0][31],headcount[1][31],headcount[2][31],headcount[3][31],headcount[4][31],headcount[5][31],headcount[6][31],headcount[7][31],headcount[8][31],headcount[9][31],headcount[10][31]]
    data['thirtythree']=[headcount[0][32],headcount[1][32],headcount[2][32],headcount[3][32],headcount[4][32],headcount[5][32],headcount[6][32],headcount[7][32],headcount[8][32],headcount[9][32],headcount[10][32]]
    data['thirtyfour']=[headcount[0][33],headcount[1][33],headcount[2][33],headcount[3][33],headcount[4][33],headcount[5][33],headcount[6][33],headcount[7][33],headcount[8][33],headcount[9][33],headcount[10][33]]
    data['thirtyfive']=[headcount[0][34],headcount[1][34],headcount[2][34],headcount[3][34],headcount[4][34],headcount[5][34],headcount[6][34],headcount[7][34],headcount[8][34],headcount[9][34],headcount[10][34]]
    data['thirtysix']=[headcount[0][35],headcount[1][35],headcount[2][35],headcount[3][35],headcount[4][35],headcount[5][35],headcount[6][35],headcount[7][35],headcount[8][35],headcount[9][35],headcount[10][35]]
    data['thirtyseven']=[headcount[0][36],headcount[1][36],headcount[2][36],headcount[3][36],headcount[4][36],headcount[5][36],headcount[6][36],headcount[7][36],headcount[8][36],headcount[9][36],headcount[10][36]]
    data['thirtyeight']=[headcount[0][37],headcount[1][37],headcount[2][37],headcount[3][37],headcount[4][37],headcount[5][37],headcount[6][37],headcount[7][37],headcount[8][37],headcount[9][37],headcount[10][37]]
    data['thirtynine']=[headcount[0][38],headcount[1][38],headcount[2][38],headcount[3][38],headcount[4][38],headcount[5][38],headcount[6][38],headcount[7][38],headcount[8][38],headcount[9][38],headcount[10][38]]
    data['forty']=[headcount[0][39],headcount[1][39],headcount[2][39],headcount[3][39],headcount[4][39],headcount[5][39],headcount[6][39],headcount[7][39],headcount[8][39],headcount[9][39],headcount[10][39]]
    data['fortyone']=[headcount[0][40],headcount[1][40],headcount[2][40],headcount[3][40],headcount[4][40],headcount[5][40],headcount[6][40],headcount[7][40],headcount[8][40],headcount[9][40],headcount[10][40]]
    data['fortytwo']=[headcount[0][41],headcount[1][41],headcount[2][41],headcount[3][41],headcount[4][41],headcount[5][41],headcount[6][41],headcount[7][41],headcount[8][41],headcount[9][41],headcount[10][41]]
    data['fortythree']=[headcount[0][42],headcount[1][42],headcount[2][42],headcount[3][42],headcount[4][42],headcount[5][42],headcount[6][42],headcount[7][42],headcount[8][42],headcount[9][42],headcount[10][42]]
    data['fortyfour']=[headcount[0][43],headcount[1][43],headcount[2][43],headcount[3][43],headcount[4][43],headcount[5][43],headcount[6][43],headcount[7][43],headcount[8][43],headcount[9][43],headcount[10][43]]
    data['fortyfive']=[headcount[0][44],headcount[1][44],headcount[2][44],headcount[3][44],headcount[4][44],headcount[5][44],headcount[6][44],headcount[7][44],headcount[8][44],headcount[9][44],headcount[10][44]]
    data['fortysix']=[headcount[0][45],headcount[1][45],headcount[2][45],headcount[3][45],headcount[4][45],headcount[5][45],headcount[6][45],headcount[7][45],headcount[8][45],headcount[9][45],headcount[10][45]]
    data['fortyseven']=[headcount[0][46],headcount[1][46],headcount[2][46],headcount[3][46],headcount[4][46],headcount[5][46],headcount[6][46],headcount[7][46],headcount[8][46],headcount[9][46],headcount[10][46]]
    data['fortyeight']=[headcount[0][47],headcount[1][47],headcount[2][47],headcount[3][47],headcount[4][47],headcount[5][47],headcount[6][47],headcount[7][47],headcount[8][47],headcount[9][47],headcount[10][47]]
    data['fortynine']=[headcount[0][48],headcount[1][48],headcount[2][48],headcount[3][48],headcount[4][48],headcount[5][48],headcount[6][48],headcount[7][48],headcount[8][48],headcount[9][48],headcount[10][48]]
    data['fifty']=[headcount[0][49],headcount[1][49],headcount[2][49],headcount[3][49],headcount[4][49],headcount[5][49],headcount[6][49],headcount[7][49],headcount[8][49],headcount[9][49],headcount[10][49]]
    data['fiftyone']=[headcount[0][50],headcount[1][50],headcount[2][50],headcount[3][50],headcount[4][50],headcount[5][50],headcount[6][50],headcount[7][50],headcount[8][50],headcount[9][50],headcount[10][50]]
    data['fiftytwo']=[headcount[0][51],headcount[1][51],headcount[2][51],headcount[3][51],headcount[4][51],headcount[5][51],headcount[6][51],headcount[7][51],headcount[8][51],headcount[9][51],headcount[10][51]]
    data['fiftythree']=[headcount[0][52],headcount[1][52],headcount[2][52],headcount[3][52],headcount[4][52],headcount[5][52],headcount[6][52],headcount[7][52],headcount[8][52],headcount[9][52],headcount[10][52]]
    data['fiftyfour']=[headcount[0][53],headcount[1][53],headcount[2][53],headcount[3][53],headcount[4][53],headcount[5][53],headcount[6][53],headcount[7][53],headcount[8][53],headcount[9][53],headcount[10][53]]
    data['fiftyfive']=[headcount[0][54],headcount[1][54],headcount[2][54],headcount[3][54],headcount[4][54],headcount[5][54],headcount[6][54],headcount[7][54],headcount[8][54],headcount[9][54],headcount[10][54]]
    data['fiftysix']=[headcount[0][55],headcount[1][55],headcount[2][55],headcount[3][55],headcount[4][55],headcount[5][55],headcount[6][55],headcount[7][55],headcount[8][55],headcount[9][55],headcount[10][55]]
    data['fiftyseven']=[headcount[0][56],headcount[1][56],headcount[2][56],headcount[3][56],headcount[4][56],headcount[5][56],headcount[6][56],headcount[7][56],headcount[8][56],headcount[9][56],headcount[10][56]]
    data['fiftyeight']=[headcount[0][57],headcount[1][57],headcount[2][57],headcount[3][57],headcount[4][57],headcount[5][57],headcount[6][57],headcount[7][57],headcount[8][57],headcount[9][57],headcount[10][57]]
    data['fiftynine']=[headcount[0][58],headcount[1][58],headcount[2][58],headcount[3][58],headcount[4][58],headcount[5][58],headcount[6][58],headcount[7][58],headcount[8][58],headcount[9][58],headcount[10][58]]
    data['sixty']=[headcount[0][59],headcount[1][59],headcount[2][59],headcount[3][59],headcount[4][59],headcount[5][59],headcount[6][59],headcount[7][59],headcount[8][59],headcount[9][59],headcount[10][59]]
    
    return data











































