from flask import Flask, request
import json
import uuid
import os

app = Flask(__name__)

DATABASE_PATH=os.environ.get('DATABASE_PATH', 'dive_locations.json')

class DiveLocation(object):
	def __init__(self, name, lat, lon, depth, _id=None):
		self.name = name
		self.lat = lat
		self.lon = lon
		self.depth = depth
		self._id = _id

	def as_json(self):
		return {
			"_id": self._id,
			"name": self.name,
			"lat": self.lat,
			"lon": self.lon,
			"depth": self.depth
		}

@app.route('/dives', methods=['GET'])
def get_all():
	diveLocs = getCollection()
	return json.dumps(diveLocs, indent=True)

@app.route('/dives/<name>', methods=['GET'])
def get_by_name(name):
	diveLocs = getCollection()
	diveLoc = find_object_in_json(diveLocs, name)
	if diveLoc:
		return json.dumps(diveLoc, indent=True)
	else:
		'''Empty response'''
		return '{}', 200

@app.route('/dives', methods=['POST'])
def add():
	try:
		payload = json.loads(request.data)
	except ValueError:
		return error("Dive locations must be specified in JSON format")
		
	'''Parameters check'''
	errorMessage = checkParameters(payload) 
	if errorMessage:
		return error(errorMessage)
	
	'''Existing location check'''	
	existingLoc = find_object_in_json(getCollection(), payload['name'])
	if existingLoc:
		return error("There is already a dive location with specified name")
	
	id = uuid.uuid4()
	newLoc = DiveLocation(payload['name'], payload['lat'], payload['lon'], payload['depth'], str(id))
	newLocJson = newLoc.as_json()
	'''Write on file'''
	updateCollection(newLocJson)
	return json.dumps(newLocJson, indent=True)

def error(message):
	return {
		"error": message
	}, 400

def checkParameters(payload):
	if 'name' not in payload:
		return "Dive locations must contain a name"
	if 'lat' not in payload:
		return "Dive locations must contain a latitude"
	if 'lon' not in payload:
		return "Dive locations must contain a longitude"
	return None

def find_object_in_json(diveLocations, name):
	for diveLoc in diveLocations:
		if diveLoc['name'] == name:
			return diveLoc
	return None
		
def getCollection():
	with open(DATABASE_PATH) as f:
		return json.load(f)

def updateCollection(diveLocationJson):
	divesList = getCollection()
	divesList.append(diveLocationJson)
	with open(DATABASE_PATH, 'w') as f:
		json.dump(divesList, f)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
