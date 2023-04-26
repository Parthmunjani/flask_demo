from flask_restful import Api,Resource

class Show(Resource):
    def get(self):
        return {"status":True,"detail":"How Are You"}
    

class Index(Resource):
    def get(self):
        return {"status":True,"detail":"Hello World"}
