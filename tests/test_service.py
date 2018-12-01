import sys
import json
import unittest
sys.path.append("..")
import service

class TestServiceApi(unittest.TestCase):
    
    def setUp(self):
        self.serviceapp = service.app.test_client()
        '''Flush sample json file'''
        with open('dive_locations.json', 'w') as f:
            f.write('[]')
    
    def test_when_getAllAtFirst_then_emptyResponse(self):
        assert self.apiGetAll(200) == []
    
    def test_when_postOneDive_then_notEmptyGets(self):
        newDiveJson = '{"name": "San Andres", "lat": "36.0144638", "lon": "-5.6090361", "depth": "34"}'
        newDive = self.apiPost(newDiveJson, 200)
                
        '''Check created data'''
        assert newDive['name'] == 'San Andres'
        assert newDive['lat'] == '36.0144638'
        assert newDive['lon'] == '-5.6090361'
        assert newDive['depth'] == '34'
        
        '''Check overall size of the collection after adding a new one'''
        assert len(self.apiGetAll(200)) == 1
        
        '''Check that exists that specific dive'''
        id = newDive['_id']
        retrievedDive = self.apiGet('San Andres', 200)
        
        assert retrievedDive['_id'] == id
        
    def apiGetAll(self, expectedCode):
        response = self.serviceapp.get("/dives")
        assert response.status_code == expectedCode
        return json.loads(response.data)
    
    def apiGet(self, name, expectedCode):
        response = self.serviceapp.get("/dives/" + name)
        assert response.status_code == expectedCode
        return json.loads(response.data)
    
    def apiPost(self, data, expectedCode):
        response = self.serviceapp.post("/dives", data=data)
        assert response.status_code == expectedCode
        return json.loads(response.data)        
        
if __name__ == '__main__':
      unittest.main()