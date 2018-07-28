from flask import Flask, render_template, jsonify, request, redirect
import pymongo

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

	print (user_dict)

	key = insert_user(user_dict)
	found_match = match(key)

	if found_match:
		return redirect ("/matches")

@app.route("/matches") # found matches
def success():
	#input info of matches to html page
    return render_template("matches.html")

def get_image_list(pic_name):
	#insert olivia's code
	return

def insert_user(user_dict):
	db.userinfo.insert(user_dict)
	return user_dict['_id']

def match(user):
	#insert tiff's algorithm thing
	return

app.run( debug = True )