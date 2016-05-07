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
	crud.print_msg(json)
	crud.add_record(json)
	return


if __name__ == '__main__':
	app.run(port=8000)
