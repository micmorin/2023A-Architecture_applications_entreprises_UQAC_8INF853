from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from db_mod import db
from ORM import User
import requests
import os
from influxdb_client import InfluxDBClient
from json import loads

def login():
    if request.method == 'POST': 
        form = request.form
        try:
            user = db.session.execute(db.select(User).filter_by(Username=form["username"])).scalar_one()
            if user.Password == form["password"]:
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash("Invalid Password. Please Try again")
        except:
            flash("Invalid User. Please Try again")

        return render_template("login.html")
    
    return render_template("login.html")

@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@login_required
def index():
    query_api = getClient().query_api()

    query = """from(bucket: \""""+getBucket()+"""\")
    |> range(start:-72h)
    """

    tables = query_api.query(query, getOrg())

    return render_template("index.html", tables = loads(tables.to_json()))

@login_required
def policy():
    if request.method == 'POST':
        if request.form.get('Delete') != None:
            flash(requests.post('http://manager:5000/removePolicy',json={"name":request.form.get('Name')}).json())
        
        elif request.form.get('Update') != None:
            new_policy = {
                request.form.get('Name'):{
                    "scope":request.form.get('scope'),
                    "if":{
                            "subject": request.form.get('if_Sujet'),
                            "object":  request.form.get('if_Objet'),
                            "comparison":request.form.get('comparaison_if_'+request.form.get('Name'))
                    },
                    "then":{
                        "subject": request.form.get('then_Sujet'),
                        "object": request.form.get('then_Objet'),
                        "action": request.form.get('comparaison_then_'+request.form.get('Name'))
                    }
                }
            }
            flash(requests.post('http://manager:5000/updatePolicy',json=new_policy).json())
        
        elif request.form.get('Add') != None:
            new_policy = {
                request.form.get('Name'):{
                    "scope":request.form.get('scope'),
                    "if":{
                            "subject": request.form.get('if_Sujet'),
                            "object":  request.form.get('if_Objet'),
                            "comparison":request.form.get('comparaison_if_')
                    },
                    "then":{
                        "subject": request.form.get('then_Sujet'),
                        "object": request.form.get('then_Objet'),
                        "action": request.form.get('comparaison_then_')
                    }
                }
            }
            flash(requests.post('http://manager:5000/addPolicy',json=new_policy).json())
            
    r = requests.get('http://manager:5000/getPolicies').json()
    return render_template('policy.html', policies=r)

def getClient():
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "my-org"
    url = "http://db:8086"
    return InfluxDBClient(url=url, token=token, org=org)

def getOrg():
    return "my-org"

def getBucket():
    return "my-bucket"