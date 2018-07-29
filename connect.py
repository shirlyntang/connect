from flask import Flask, render_template, jsonify, request, redirect, json
import pymongo, math

uri = 'mongodb://connect:connect123@ds157901.mlab.com:57901/userinfo' #connect to database

client = pymongo.MongoClient(uri)

db = client.get_default_database()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form")
def form_func():
    return render_template("form.html")

@app.route("/create_profile", methods=["POST"]) # page where user fills out form
def get_user_info():

    found_match = False
    key = '';
    fields = ['username', 'name', 'age', 'school', 'hobbies', 'animals', 'foods', 'phone_number', 'pic'] #can add more

    user_dict = {} # creates empty dictionary

    for category in fields: # adds answers to all fields into dictionary

        if category == 'username':
            user_dict['_id'] = request.form[category]

        elif category == 'hobbies' or category == 'foods' or category == 'animals':
            user_dict[category] = [word.strip() for word in request.form[category].split(',')]

        elif category == 'phone_number':
            number = request.form[category].replace('()', '')
            if len(number) == 11 and number[0] == '1':
                number = number[1:]
            number = '(' + number[0:3] + ')' + number[3:6] + '-' + number[6:]
            user_dict[category] = number

        elif category == 'pic':
            user_dict[category] = get_image_list(request.form[category])

        else:
            user_dict[category] = request.form[category]

        if category == 'name':
            user_dict[category] = user_dict[category].title() # makes first letter of each word uppercase
        elif category == 'username' or category == 'pic':
            pass
        elif category == 'hobbies' or category == 'foods' or category == 'animals':
            for word in user_dict[category]:
                word = word.lower()
        else:
            user_dict[category] = user_dict[category].lower()

    user_dict['other_matches'] = [];

    key = insert_user(user_dict)
    found_match = match(key)

    if found_match:
        return success(user_dict['_id'])
        #return redirect ("/matches")
    return redirect("/fail")

@app.route("/matches", methods = ["GET"]) # found matches
def success(user_key):
    #input info of matches to html page
    user = db.userinfo.find_one({'_id': user_key})
    print (user['other_matches'])
    if len(user['other_matches'])>0:
        matched_user_key = user['other_matches'][len(user['other_matches'])-1]
        matched_user = db.userinfo.find_one({'_id': matched_user_key})
        print ("\n\n")
        print (matched_user)
        print ("\n\n")
        return render_template("matches.html", 
            pic = matched_user['pic'],
            name = matched_user['name'], 
            age = matched_user['age'], 
            school = matched_user['school'], 
            hobbies = matched_user['hobbies'], 
            animals = matched_user['animals'], 
            foods = matched_user['foods']
        )
    return render_template("matches.html")

@app.route("/fail")
def fail():
    return render_template("fail.html")

def get_image_list(pic_name):
    #insert olivia's code
    return ['sample']

def insert_user(user_dict):
    db.userinfo.insert(user_dict)
    return user_dict['_id']

def compare(person,potential):
    points = 0
    for person_att in person:
        for potential_att in potential:
            if(person_att.lower() == potential_att.lower()):
                points = points + 1
    return points

def similar(person,all_user_data):

    similarity_points = dict()

    for potential in all_user_data:
        if potential['_id'] == person['_id'] or person['_id'] in potential["other_matches"]:
            similarity_points[potential['_id']]=-1
        else:
            #compare age. the older the age gap the better.
            similarity_points[potential['_id']]=similarity_points.get(potential['_id'],0) + math.fabs(int(person['age'])-int(potential['age']))

            #compare school. potentially implement geographic location / other similarity.
            if(person['school'].lower() == potential['school'].lower()):
                similarity_points[potential['_id']]=similarity_points.get(potential['_id'],0)+1

            #compare hobbies
            similarity_points[potential['_id']]=similarity_points.get(potential['_id'],0)+compare(person['hobbies'],potential['hobbies'])

            #compare animal
            similarity_points[potential['_id']]=similarity_points.get(potential['_id'],0)+compare(person['animals'],potential['animals'])

            #compare food
            similarity_points[potential['_id']]=similarity_points.get(potential['_id'],0)+compare(person['foods'],potential['foods'])

            #similarity_points{people['_id'],similarity_points.get(people['_id']) + get_picture_similarity}
    
    highest = -1
    match = ""
    for key, value in similarity_points.iteritems():
        if(value > highest):
            highest = value
            match = key

    return match

def match(user_key):

    all_user_data = [ user for user in db.userinfo.find() ]

    user = db.userinfo.find_one({'_id': user_key})

    match = similar(user,all_user_data)

    for person in all_user_data:
        if match == person['_id']:
            db.userinfo.update({'_id':user_key}, {'$push': {'other_matches': match}})
            return True
    return False

app.run( debug = True )