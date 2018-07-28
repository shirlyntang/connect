from flask import Flask, render_template, jsonify, request, redirect
import pymongo

uri = 'mongodb://connect:connect123@ds157901.mlab.com:57901/userinfo' #connect to database

client = pymongo.MongoClient(uri)

db = client.get_default_database()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create_profile", methods=["POST"]) # page where user fills out form
def get_user_info():

	bool found_match = False
	key = '';
	fields = ['name', 'age', 'school', 'hobbies', 'animal', 'food', 'phone_number', 'picture'] #can add more

	user_dict = {} # creates empty dictionary

	for category in fields: # adds answers to all fields into dictionary

		if category == 'hobbies': # can add other fields to this
			user_dict[category] = [word.strip() for word in request.form[category].split(',')]

		elif category == 'phone_number':
			number = request.form[category].translate(None, ', ')
			if len(number) == 11 && number[0] = '1':
				number = number[1:]
			number = '(' + number[0:3] + ')' + number[3:6] + '-' + number[6:]
			user_dict[category] = number

		elif category == 'picture'
			user_dict[category] = get_image_list(request.form[category])

		else:
			user_dict[category] = request.form[category]

	key = insert_user(user_dict)
	found_match = match(key)
	
	if found_match:
		return redirect ("/success")
	return redirect("/found")

@app.route("/success") # found matches
def success():
    return render_template("success.html")

def get_image_list(pic_name):
	#insert olivia's code

def insert_user(user_dict):
	db.userinfo.insert(user_dict)
	return user_key

def match(user):
	#insert tiff's algorithm thing

app.run( debug = True )