from re import RegexFlag
from flask import Flask,json, render_template, url_for, request, redirect, session
from pymongo import MongoClient
import bcrypt
import requests
import dns.resolver
from bson import ObjectId
from json2html import *
from os import linesep


dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = MyEncoder
app.secret_key = 'amsdasdjapodj apsdoj paosjd'

cluster = MongoClient(
    "mongodb+srv://BalaAyyappan:bala@nutritionassistant.97pdlqy.mongodb.net/?retryWrites=true&w=majority")

db = cluster.Nutrition_Ass
collection = db.users


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Profile', methods=['POST', 'GET'])
def profile():
    # Calorie Ninja
    # "X-RapidAPI-Key": "aa95b88b45mshe4394a422ce8c48p13a698jsn9d8eb019e144",
    #  "X-RapidAPI-Host": "calorieninjas.p.rapidapi.com"   
    url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"

    headers = {
        "X-RapidAPI-Key": "aa95b88b45mshe4394a422ce8c48p13a698jsn9d8eb019e144",
        "X-RapidAPI-Host": "calorieninjas.p.rapidapi.com"
    }

    if request.method == 'POST':
        foodname = request.form['foodname']

        querystring = {"query": foodname}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        json_data = response.text
        infoFromJson = json.loads(json_data)
        #result = pd.DataFrame(infoFromJson['items'])
        #print(result)
        new_data = list(infoFromJson.items())
        print(type(new_data))
        final_data=new_data[0][1]
        line = '\n'
        gram = 'g'
        miligram = 'm'
        for datas in final_data:
            result = f"Name : {datas['name'].capitalize()}"
            result1 = f"Protein : {datas['protein_g']}{gram}"  
            result2 = f"Calories : {datas['calories']}"
            result3 =  f"Carbohydrates : {datas['carbohydrates_total_g']}{gram}"
            result4 =  f"Sugar : { datas['sugar_g']}{gram}"
            result5 = f"fiber : {datas['fiber_g']}{gram}"
            result6 = f"Fat : {datas['fat_total_g']}{gram}"
            result7 =  f"Cholesterol : {datas['cholesterol_mg']}{miligram}{gram}"
            
            return render_template('profile.html',line= line, result=result, result1=result1, result2=result2, result3=result3, result4=result4, result5=result5, result6=result6, result7=result7)
        
    return render_template("profile.html")
    

@app.route('/Forget Password')
def fyp():
    return render_template("fyp.html")      


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = db.collection.users
        username = request.form["username"]

        # check credentials
        login_user = user.find_one({'Name': username})
        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['Password']) == login_user['Password']:
                session["username"] = username
                return render_template("profile.html")
               
            else:
                return render_template("login.html")
        else:
            return render_template("login.html") 
    else:
        return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = db.collection.users
        existing_user = user.find_one(
            {'name': request.form['username']})

        if existing_user is None:
            x = "already a user"
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            user.insert_one(
                {'Name': request.form['username'], 'Password': hashpass, 'City': request.form["city"], 'Gender': request.form["gender"], 'Age': request.form["age"], 'Activity': request.form["activity"],
                    'Height': request.form["height"], 'Weight': request.form["weight"], 'Weight_loss': request.form["Weight_loss"], "Goal": request.form["goal"]})
            session['username'] = request.form['username']
            return redirect(url_for('login'))
            
        return render_template('register.html', x=x) 

    return render_template('register.html')

    


if __name__ == "__main__":
    app.run(debug=True)
