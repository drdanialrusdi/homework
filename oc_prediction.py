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
        today=dayarray[currentday(),:]
        fullhour=19
    else:
        today=[]
        fullhour=13
    Pred_memory=[]
    Full_prediction=[]
    
    for pred in range(11):
        data2=data[0,:11-pred]
        
        if len(Pred_memory)!=0:
            data2=np.insert(data2,0,Pred_memory)
        data2=data2.reshape(1,len(data2))
        data_to_predict=np.concatenate((data2,[today],timearray[pred,:].reshape(1,11)),axis=1)
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
    
    pred=oc_predict_simulation(data,new_data=[],model_select=model_select)
    data={}
    if len(pred)==5:
        pred.extend(['NaN']*6)
    new_data.extend(['NaN']*(11-len(new_data)))
    data['title']=model_select
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















































