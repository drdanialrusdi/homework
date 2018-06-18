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

yesterday_data_eftb#function to return yesterday_data
yesterday_data_egtb#function to return pasthourdata
yesterday_data_egib
yesterday_data_elib
yesterday_data_elbb
yesterday_data_egbb

pasthourdata_eftb
pasthourdata_egtb
pasthourdata_egib
pasthourdata_elib
pasthourdata_elbb
pasthourdata_egbb

data_eftb=oc_dict(data=yesterday_data_eftb,new_data=pasthourdata_eftb,model_select='EFTB', models=EFTBS)
data_egtb=oc_dict(data=yesterday_data_egtb,new_data=pasthourdata_egtb,model_select='EGTB', models=EGTBS)
data_egib=oc_dict(data=yesterday_data_egib,new_data=pasthourdata_egib,model_select='EGIB', models=EGIBS)
data_elib=oc_dict(data=yesterday_data_elib,new_data=pasthourdata_elib,model_select='ELIB', models=ELIBS)
data_elbb=oc_dict(data=yesterday_data_elbb,new_data=pasthourdata_elbb,model_select='ELBB', models=ELBBS)
data_egbb=oc_dict(data=yesterday_data_egbb,new_data=pasthourdata_egbb,model_select='EGBB', models=EGBBS)






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
        global data_eftb
		global yesterday_data_eftb
		global pasthourdata_eftb
		#if function pasthourdata_eftb != pasthourdata_eftb | function yesterday_data_eftb != yesterday_data_eftb:
			#pasthourdata_eftb=function pasthourdata
			#yesterday_data_eftb=function yesterday_data
			#data_eftb=oc_dict(data=yesterday_data_eftb,new_data=pasthourdata_eftb,model_select='EFTB', models=EFTBS)data_eftb=oc_dict(data=yesterday_data_eftb,new_data=pasthourdata_eftb,model_select='EFTB', models=EFTBS)
		
        return render_template('main_template.html' ,data=data_eftb)

@app.route('/EGTB')
def EGTB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        global data_egtb
		global yesterday_data_egtb
		global pasthourdata_egtb
		#if function pasthourdata_egtb != pasthourdata_egtb | function yesterday_data_egtb != yesterday_data_egtb:
		#pasthourdata_eftb=function pasthourdata
			#yesterday_data_eftb=function yesterday_data
			#data_egtb=oc_dict(data=yesterday_data_egtb,new_data=pasthourdata_egtb,model_select='EGTB', models=EGTBS)
        return render_template("main_template.html" ,data=data_egtb)

@app.route('/EGIB')
def EGIB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        global data_egib
        global yesterday_data_egib
		global pasthourdata_egib
		#if function pasthourdata_egib != pasthourdata_egib | function yesterday_data_egib != yesterday_data_egib:
		#pasthourdata_eftb=function pasthourdata
			#yesterday_data_eftb=function yesterday_data
			#data_egib=oc_dict(data=yesterday_data_egib,new_data=pasthourdata_egib,model_select='EGIB', models=EGIBS)
        return render_template('main_template.html' ,data=data_egib)

@app.route('/ELIB')
def ELIB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        global data_elib
        global yesterday_data_elib
		global pasthourdata_elib
		#if function pasthourdata_elib != pasthourdata_elib | function yesterday_data_elib != yesterday_data_elib:
		#pasthourdata_eftb=function pasthourdata
			#yesterday_data_eftb=function yesterday_data
			#data_elib=oc_dict(data=yesterday_data_elib,new_data=pasthourdata_elib,model_select='ELIB', models=ELIBS)
        return render_template('main_template.html' ,data=data_elib)

@app.route('/ELBB')
def ELBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        global data_elbb
        global yesterday_data_elbb
		global pasthourdata_elbb
		#if function pasthourdata_elbb != pasthourdata_elbb | function yesterday_data_elbb != yesterday_data_elbb:
		#pasthourdata_eftb=function pasthourdata
			#yesterday_data_eftb=function yesterday_data
			#data_elbb=oc_dict(data=yesterday_data_elbb,new_data=pasthourdata_elbb,model_select='ELBB', models=ELBBS)
        return render_template('main_template.html' ,data=data_elbb)

@app.route('/EGBB')
def EGBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        global data_egbb
        global yesterday_data_egbb
		global pasthourdata_egbb
		#if function pasthourdata_egbb != pasthourdata_egbb | function yesterday_data_egbb != yesterday_data_egbb:
		#pasthourdata_eftb=function pasthourdata
			#yesterday_data_eftb=function yesterday_data
			#data_egbb=oc_dict(data=yesterday_data_egbb,new_data=pasthourdata_egbb,model_select='EGBB', models=EGBBS)
        return render_template('main_template.html' ,data=data_egbb)
    
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
    
    
    
    
    
    
    