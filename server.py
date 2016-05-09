from flask import Flask, request, jsonify, render_template
import json
import crud
app = Flask(__name__)

@app.route('/')
def index():
	 return render_template('index.html')

@app.route('/api/user/register', methods = ['POST'])
def post():
	json = request.json
	result = crud.register(json)
	return(jsonify(response=200))

@app.route('/api/print', methods = ['POST'])
def print_post():
	json = request.json
	result = crud.print_msg(json)

	return(jsonify(response=200))

@app.route('/api/mail', methods = ['POST'])
def send():
	print("Came into server")
	json = request.json
	result = crud.send(json)
	return(result)

if __name__ == '__main__':
	app.debug=True
	app.run(port=8000)
