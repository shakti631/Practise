import json
import mysql.connector
from flask import Blueprint,Flask,request,make_response,render_template
from datetime import datetime,timedelta,date,time
import jwt

app = Flask(__name__,template_folder='/templates')

def xyz(a):
    if request.method == 'POST':
        search = a['review']
        if search.find("average"):
            x = 'movie was average'
        if search.find("good"):
            x = 'movie was good'
        else:
            x = 'movie was bad'
        return render_template('call.html',result=x)
    else:
        return render_template('form.html')

@app.route("/", methods=['GET','POST'])
def abc():
    return xyz(request.form)

app.run(debug=True)