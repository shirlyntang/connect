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

		if category == 'name':
			request.form[category] = request.form[category].title() # makes first letter of each word uppercase
		else:
			request.form[category] = request.form[category].lower()

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

	user_dict['other_matches'] = [];

	print (user_dict)

	key = insert_user(user_dict)
	found_match = match(key)

	if found_match:
		return redirect ("/matches")

@app.route("/matches") # found matches
def success():
	#input info of matches to html page
    return render_template("matches.html") # insert json object as a second parameter

def get_image_list(pic_name):
	#insert olivia's code
	return

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

def similar(person,json_data):

	similarity_points = dict()

    for potential in json_data:
        if potential['id'] == person['id'] or person['id'] in potential["other_matches"]:
            similarity_points[potential['id']]=-1
        else:
            #compare age. the older the age gap the better.
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0) + math.fabs(int(person['age'])-int(potential['age']))

            #compare school. potentially implement geographic location / other similarity.
            if(person['school'].lower() == potential['school'].lower()):
                similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+1

            #compare hobbies
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+compare(person['hobbies'],potential['hobbies'])

            #compare animal
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+compare(person['animals'],potential['animals'])

            #compare food
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+compare(person['foods'],potential['foods'])

            #similarity_points{people['id'],similarity_points.get(people['id']) + get_picture_similarity}
    
    highest = 0
    match = ""
    for key, value in similarity_points.iteritems():
        if(value > highest):
            highest = value
            match = key

    return match

def match(user_key):
    data = """[{"id":"id1", "name": "Abe", "age": "22", "school":"school 1", "hobbies": ["acting"], "animals":["dog"], "foods":["apple"],"other_matches": ["hello"]},
    {"id":"id2", "name": "Bella", "age": "22", "school":"school 2", "hobbies": ["baseball"], "animals":["cat"], "foods":["apple"],"other_matches": [""]},
    {"id":"id3", "name": "Cat", "age": "21", "school":"school 3", "hobbies":["acting"], "animals":["dog"], "foods":["orange"],"other_matches": [""]},
    {"id":"id4", "name": "Dan", "age": "20", "school":"school 4", "hobbies": ["nothing"], "animals":["bunny"], "foods":["poo"],"other_matches": [""]}]"""

    json_data = json.loads(data)

    user = db.userinfo.find({'_id': user_key})

    match = similar(user,json_data)

    for person in json_data:
        if match == person['id']:
            print json_data[0]['other_matches']
            json_data[0]['other_matches'].append(match)
            print json_data[0]['other_matches']

app.run( debug = True )