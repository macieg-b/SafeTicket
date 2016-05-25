from flask import Flask, request, jsonify, render_template
import json
import crud
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/api/user/login', methods = ['POST'])
def login():
	return(crud.login(request.json))

@app.route('/api/user/pre-register', methods = ['POST'])
def pre_register():
	return(crud.pre_register(request.json))

@app.route('/api/user/register', methods = ['POST'])
def post():
	return(crud.register(request.json))

@app.route('/api/tickets/<city>', methods = ['POST'])
def cityinfo(city):
	return crud.return_CityInfo(city)

if __name__ == '__main__':
	app.debug=True
	app.run(port=8000)
	#app.run(host='0.0.0.0')

