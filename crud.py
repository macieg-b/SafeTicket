from flask import jsonify, json
import MySQLdb

hostData="us-cdbr-azure-east-a.cloudapp.net";
userData="baa57d8d1e6f72";
passData="4cb8825d";
dbData="YanosikDB";

def register(jsonArg):
	#Database connection, and select object to send queries
	db = MySQLdb.connect(host=hostData,
                 	     user=usetData,
                	     passwd=passData,
                    	 db=dbData)
	cur=db.cursor()

	#Parse jsonArg to proper variables
	longitude=arg['x']
	lattitude=arg['y']

	#Execute proper queries
	cur.execute("INSERT INTO cords (id, longitude, latitude) VALUES (6, 11.11, 22.22)")
return
