# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:14:08 2018

@author: 00130161
"""
from  flask import Flask, request, url_for, redirect, render_template
from datetime import datetime, date, timedelta
from oc_prediction import *
from oc_simulation import *
import pyodbc
import time
import pandas as pd

#Function to retrieve data from database


app = Flask(__name__)

df=pd.read_excel("data_model\\Call Duration and Incoming Call.xlsx")
duration_eftb=df['Duration_EFTB'].dropna().tolist()
duration_egtb=df['Duration_EGTB'].dropna().tolist()
duration_egib=df['Duration_EGIB'].dropna().tolist()
duration_elib=df['Duration_ELIB'].dropna().tolist()
duration_elbb=df['Duration_ELBB'].dropna().tolist()
duration_egbb=df['Duration_EGBB'].dropna().tolist()
incomingcall_eftb=df['IncomingCall_EFTB'].dropna().tolist()
incomingcall_egtb=df['IncomingCall_EGTB'].dropna().tolist()
incomingcall_egib=df['IncomingCall_EGIB'].dropna().tolist()
incomingcall_elib=df['IncomingCall_ELIB'].dropna().tolist()
incomingcall_elbb=df['IncomingCall_ELBB'].dropna().tolist()
incomingcall_egbb=df['IncomingCall_EGBB'].dropna().tolist()
abandoncall_eftb=df['AbandonCall_EFTB'].dropna().tolist()
abandoncall_egtb=df['AbandonCall_EGTB'].dropna().tolist()
abandoncall_egib=df['AbandonCall_EGIB'].dropna().tolist()
abandoncall_elib=df['AbandonCall_ELIB'].dropna().tolist()
abandoncall_elbb=df['AbandonCall_ELBB'].dropna().tolist()
abandoncall_egbb=df['AbandonCall_EGBB'].dropna().tolist()
outboundduration_eftb=df['OutboundCallDuration_EFTB'].dropna().tolist()
outboundduration_egtb=df['OutboundCallDuration_EGTB'].dropna().tolist()
outboundduration_egib=df['OutboundCallDuration_EGIB'].dropna().tolist()
outboundduration_elib=df['OutboundCallDuration_ELIB'].dropna().tolist()
outboundduration_elbb=df['OutboundCallDuration_ELBB'].dropna().tolist()
outboundduration_egbb=df['OutboundCallDuration_EGBB'].dropna().tolist()
probob_eftb=df['probob_EFTB'].dropna().tolist()
probob_egtb=df['probob_EGTB'].dropna().tolist()
probob_egib=df['probob_EGIB'].dropna().tolist()
probob_elib=df['probob_ELIB'].dropna().tolist()
probob_elbb=df['probob_ELBB'].dropna().tolist()
probob_egbb=df['probob_EGBB'].dropna().tolist()
outboundarrival_eftb=df['OutboundArrival_EFTB'].dropna().tolist()
outboundarrival_egtb=df['OutboundArrival_EGTB'].dropna().tolist()
outboundarrival_egib=df['OutboundArrival_EGIB'].dropna().tolist()
outboundarrival_elib=df['OutboundArrival_ELIB'].dropna().tolist()
outboundarrival_elbb=df['OutboundArrival_ELBB'].dropna().tolist()
outboundarrival_egbb=df['OutboundArrival_EGBB'].dropna().tolist()
EFTBS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='EFTB')
EGTBS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='EGTB')
EGIBS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='EGIB')
ELIBS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='ELIB')
ELBBS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='ELBB')
EGBBS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='EGBB')
ALLS=pd.read_excel("data_model\\Simulationvalue.xlsx", sheetname='ALL')

@app.route('/')
def index():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        
        return redirect('/EFTB')

@app.route('/EFTB')
def EFTB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=EFTBS
        datenow=date.today()
        yesterday_data=[7,11,28,48,31,19,55,65,55,46,13]
        pasthourdata=[4,14,9,8]
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='EFTB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/EGTB')
def EGTB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=EGTBS
        datenow=date.today()
        yesterday_data=[7,29,67,62,50,42,55,56,68,75,23]
        pasthourdata=[7,18,32,20]
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='EGTB', models=models)
        return render_template("main_template.html" ,data=data)

@app.route('/EGIB')
def EGIB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=EGIBS
        datenow=date.today()
        yesterday_data=[7,9,27,29,24,15,23,34,36,37,9]
        pasthourdata=[8,12,12,4]
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='EGIB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/ELIB')
def ELIB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=ELIBS
        datenow=date.today()
        yesterday_data=[1,8,31,43,27,11,36,33,46,28,3]
        pasthourdata=[6,4,10,6]
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='ELIB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/ELBB')
def ELBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=ELBBS
        datenow=date.today()
        yesterday_data=[0,0,38,102,77,58,90,100,114,68,3]
        pasthourdata=[6,4,10,6]
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='ELBB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/EGBB')
def EGBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=EGBBS
        datenow=date.today()
        yesterday_data=[0,0,25,60,42,25,35,44,58,35,2]
        pasthourdata=[6,4,10,6]
        data=oc_dict(data=yesterday_data,new_data=pasthourdata, model_select='EGBB', models=models)
        return render_template('main_template.html' ,data=data)
    
@app.route('/combineall')
def combineall():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=ALLS
        return render_template('main_template2.html',data=data)

@app.route('/simulation')
def simulation():
    return render_template('simulation.html')
    
@app.route('/simulationresult', methods=["POST"])
def simulationresult():
    data=request.form.to_dict()
    if data['model']=='EFTB':
        probob=probob_eftb
        outboundarrival=outboundarrival_eftb
        outboundduration=outboundduration_eftb
        incominglist=incomingcall_eftb
        durationlist=duration_eftb
        abandonlist=abandoncall_eftb
    elif data['model']=='EGTB':
        probob=probob_egtb
        outboundarrival=outboundarrival_egtb
        outboundduration=outboundduration_egtb
        incominglist=incomingcall_egtb
        durationlist=duration_egtb
        abandonlist=abandoncall_egtb
    elif data['model']=='EGIB':
        probob=probob_egib
        outboundarrival=outboundarrival_egib
        outboundduration=outboundduration_egib
        incominglist=incomingcall_egib
        durationlist=duration_egib
        abandonlist=abandoncall_egib
    elif data['model']=='ELIB':
        probob=probob_elib
        outboundarrival=outboundarrival_elib
        outboundduration=outboundduration_elib
        incominglist=incomingcall_elib
        durationlist=duration_elib
        abandonlist=abandoncall_elib
    elif data['model']=='ELBB':
        probob=probob_elbb
        outboundarrival=outboundarrival_elbb
        outboundduration=outboundduration_elbb
        incominglist=incomingcall_elbb
        durationlist=duration_elbb
        abandonlist=abandoncall_elbb
    elif data['model']=='EGBB':
        probob=probob_elbb
        outboundarrival=outboundarrival_elbb
        outboundduration=outboundduration_elbb
        incominglist=incomingcall_egbb
        durationlist=duration_egbb
        abandonlist=abandoncall_egbb
    
    a,b=number_of_simulation(n_simulation=int(data['simulation_number']),incominglist=incominglist, durationlist=durationlist, num_call=int(data['offered_call']), abandonlist=abandonlist,max_agent=int(data['number_agent']),  numcall_follow_poisson=False)
    abandonpercentage={}
    print(b)
    for n,item in enumerate(b):
        abandonpercentage[str(n)+ " agent"]=np.round(item,4)
    return render_template('simulationresult.html', data=abandonpercentage)
    
if __name__ == "__main__":
    app.run(port=5000)  
    #host='0.0.0.0',port=5000
    
    
    
    
    
    
    