from flask import Flask, request, jsonify, render_template
import json
import crud
import show_db

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

@app.route('/api/tickets/<city>', methods = ['GET'])
def cityinfo(city):
	return crud.return_city_info(city)

@app.route('/api/tickets/timeticket', methods = ['POST'])
def time_ticket():
	return (crud.buyTimeTicket(request.json))

@app.route('/api/tickets-dictionary/<city>', methods = ['POST', 'GET'])
def ticketdictionary(city):
	return crud.return_ticket_dictionary(city)

@app.route('/database', methods = ['GET'])
def show():
	return render_template('showDB.html', data=show_db.SelectAll())


if __name__ == '__main__':
	app.debug=True
	app.run(port=8000)
	#app.run(host='0.0.0.0')
