from flask import Flask, render_template, jsonify, request
import pymongo

uri = 'mongodb://connect:connect123@ds157901.mlab.com:57901/userinfo' #connect to database

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hi", methods=["POST"]) #example (change later)
def anything():
	print(request.form['name'])
	return jsonify({"name": "lorman"})


app.run( debug = True )


def main(args):

    client = pymongo.MongoClient(uri)

    db = client.get_default_database()
    
    # insert data

    client.close()
