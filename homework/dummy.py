# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 08:28:22 2018

@author: 00130161
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:14:08 2018

@author: 00130161
"""
from  flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

a=12

@app.route('/')
def index():
    global a
    if a==12:
        a=14
        return 'done'
    elif a==14:
        a=12
        return 'change'

if __name__ == "__main__":
    app.run(port=5000)  
    #host='0.0.0.0',port=5000
    