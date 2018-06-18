# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:14:08 2018

@author: 00130161
"""
from  flask import Flask, request, url_for, redirect, render_template
from datetime import datetime, date, timedelta
from oc_prediction import *
from oc_simulation import *
from pyodbc_code import *
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


@app.route('/')
def index():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        
        return redirect('/EFTB')

@app.route('/EFTB')
def EFTB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        models=EFTBS
        datenow=date.today()
        yesterday_data=extractbasedata(model_select='EFTB',datadate=datenow)
        pasthourdata=extracttodaydata(model_select='EFTB',datadate=datenow)
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='EFTB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/EGTB')
def EGTB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        models=EGTBS
        datenow=date.today()
        yesterday_data=extractbasedata(model_select='EGTB',datadate=datenow)
        pasthourdata=extracttodaydata(model_select='EGTB',datadate=datenow)
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='EGTB', models=models)
        return render_template("main_template.html" ,data=data)

@app.route('/EGIB')
def EGIB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        models=EGIBS
        datenow=date.today()
        yesterday_data=extractbasedata(model_select='EGIB',datadate=datenow)
        pasthourdata=extracttodaydata(model_select='EGIB',datadate=datenow)
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='EGIB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/ELIB')
def ELIB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        models=ELIBS
        datenow=date.today()
        yesterday_data=extractbasedata(model_select='ELIB',datadate=datenow)
        pasthourdata=extracttodaydata(model_select='ELIB',datadate=datenow)
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='ELIB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/ELBB')
def ELBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=ELBBS
        datenow=date.today()
        yesterday_data=extractbasedata(model_select='ELBB',datadate=datenow)
        pasthourdata=extracttodaydata(model_select='ELBB',datadate=datenow)
        data=oc_dict(data=yesterday_data,new_data=pasthourdata,model_select='ELBB', models=models)
        return render_template('main_template.html' ,data=data)

@app.route('/EGBB')
def EGBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        models=EGBBS
        datenow=date.today()
        yesterday_data=extractbasedata(model_select='EGBB',datadate=datenow)
        pasthourdata=extracttodaydata(model_select='EGBB',datadate=datenow)
        data=oc_dict(data=yesterday_data,new_data=pasthourdata, model_select='EGBB', models=models)
        return render_template('main_template.html' ,data=data)
    
@app.route('/simulation')
def simulation():
    return render_template('simulation.html')
    
@app.route('/simulationresult', methods=["POST"])
def simulationresult():
    data=request.form.to_dict()
    if data['model']=='EFTB':
        incominglist=incomingcall_eftb
        durationlist=duration_eftb
        abandonlist=abandoncall_eftb
    elif data['model']=='EGTB':
        incominglist=incomingcall_egtb
        durationlist=duration_egtb
        abandonlist=abandoncall_egtb
    elif data['model']=='EGIB':
        incominglist=incomingcall_egib
        durationlist=duration_egib
        abandonlist=abandoncall_egib
    elif data['model']=='ELIB':
        incominglist=incomingcall_elib
        durationlist=duration_elib
        abandonlist=abandoncall_elib
    elif data['model']=='ELBB':
        incominglist=incomingcall_elbb
        durationlist=duration_elbb
        abandonlist=abandoncall_elbb
    elif data['model']=='EGBB':
        incominglist=incomingcall_egbb
        durationlist=duration_egbb
        abandonlist=abandoncall_egbb
    
    a,b=number_of_simulation(n_simulation=int(data['simulation_number']),incominglist=incominglist, durationlist=durationlist, num_call=int(data['offered_call']), abandonlist=abandonlist,max_agent=int(data['number_agent']),  numcall_follow_poisson=False)
    abandonpercentage={}
    for n,item in enumerate(b):
        abandonpercentage[str(n)+ " agent"]=item
    return render_template('simulationresult.html', data=abandonpercentage)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)  
    
    
    
    
    
    
    
    