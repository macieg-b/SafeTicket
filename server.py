from flask import Flask, request, jsonify, render_template
import json
import crud
app = Flask(__name__)

@app.route('/')
def index():
	 return render_template('index.html')

@app.route('/api/register', methods = ['POST'])
def register():
	json = request.json
	crud.print_msg(json)
	crud.add_record(json)
	return

@app.route('/api/tickets/<city>', methods = ['POST'])
def cityinfo(city):
	return crud.return_CityInfo(city);

@app.route('/api/user/activate', methods = ['POST'])
def Activate():
	return crud.user_Activate(request.json);


if __name__ == '__main__':
	app.debug = True
	app.run(port=8000)
