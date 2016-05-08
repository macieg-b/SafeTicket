from flask import Flask, request, jsonify, render_template
import json
import crud
app = Flask(__name__)

@app.route('/')
def index():
	 return render_template('index.html')

@app.route('/api/register', methods = ['POST'])
def post():
	json = request.json
	result = crud.register(json)
	return(jsonify(response=200))

@app.route('/api/print', methods = ['POST'])
def print_post():
	json = request.json
	result = crud.print_msg(json)

	return(jsonify(response=200))

if __name__ == '__main__':
	app.run(port=8000)
