"""
TODO:
-marshal output using marshmallow (particularly for PatientsResource)
-^return Response with status code and content 
-fix put method, current update results in 'database locked'
-consider adding patch method
-add blood pressure (consists of 2 values)
-split into app.py and APIS.py
"""


from flask import Flask, Response
from flask_restful import Api,Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PatientModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    temperature = db.Column(db.Float)
    pulse = db.Column(db.Float)
    oxi = db.Column(db.Float)
    weight = db.Column(db.Float)
    gluco = db.Column(db.Float)
    # def update(self,readings:dict) -> None:
    #     if readings['temperature'] is not None:
    #         self.temperature = readings['temperature']
    #     if readings['pulse'] is not None:
    #         self.pulse = readings['pulse']
    #     if readings['oxi'] is not None:
    #         self.oxi = readings['oxi']
    #     if readings['weight'] is not None:
    #         self.weight = readings['weight']
    #     if readings['gluco'] is not None:
    #         self.gluco = readings['gluco']
        
    def __repr__(self):
        rep = f"Patient(id = {self.id}, temperature = {self.temperature}, pulse = {self.pulse}, oxi = {self.oxi}, weight = {self.weight}, gluco = {self.gluco})"
        return rep

db.create_all()

patient_fields = {
    'id': fields.Integer,
    # 'bp': fields.List,
    'temperature': fields.Float,
    'pulse': fields.Float,
    'oxi': fields.Float,
    'weight': fields.Float,
    'gluco': fields.Float
}

put_args = reqparse.RequestParser(bundle_errors=True)
put_args.add_argument('temperature', type=float, help='Invalid Temperature')
# put_args.add_argument('bp',type=list, location=json, help='Invalid Blood Pressure')
put_args.add_argument('pulse', type=float, help='Invalid Pulse')
put_args.add_argument('oxi',type=float, help='Invalid Oximeter')
put_args.add_argument('weight',type=float, help='Invalid Weight')
put_args.add_argument('gluco',type=float, help='Invalid Glucometer')

class PatientResource(Resource):
    # Read
    @marshal_with(patient_fields)
    def get(self,patientID):
        result = PatientModel.query.get(patientID)
        # if result is None:
        #     return Response(status=404)
        # else:
        #     return Response(status=200)
        return result

    # Update/Create
    @marshal_with(patient_fields)
    def put(self,patientID):
        patient = PatientModel.query.get(patientID)
        args = put_args.parse_args()
        if patient is None:
            patient = PatientModel(
                id = patientID,
                temperature = args['temperature'],
                pulse = args['pulse'],
                oxi = args['oxi'],
                weight = args['weight'],
                gluco = args['gluco']
            )
            db.session.add(patient)
            db.session.commit()
        else:
            # need to fix, 'database locked'
            updated_readings = {}
            for key in args.keys():
                val = args[key]
                if val is not None:
                    updated_readings[key] = val
            db.session.query(PatientModel).filter(PatientModel.id == patientID).update(updated_readings) 
            db.session.commit()
        return patient

    # Delete
    @marshal_with(patient_fields)
    def delete(self,patientID):
        patient = PatientModel.query.get_or_404(patientID)
        db.session.delete(patient)
        db.session.commit()
        return patient

class PatientsResource(Resource):
    # Read
    # need to marshal output
    def get(self):
        result = PatientModel.query.all()
        return result

api.add_resource(PatientResource,'/patients/<int:patientID>')
api.add_resource(PatientsResource,'/patients')

if __name__ == '__main__':
    app.run(debug=True)