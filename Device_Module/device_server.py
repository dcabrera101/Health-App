"""
TODO:
-marshal output using marshmallow
-split into application.py and APIS.py
-fix bugs with put method
"""


from flask import Flask, Response
from flask_restful import Api,Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
db = SQLAlchemy(application)

class PatientModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    temperature = db.Column(db.Float)
    pulse = db.Column(db.Float)
    oxi = db.Column(db.Float)
    weight = db.Column(db.Float)
    gluco = db.Column(db.Float)        
    def __repr__(self):
        rep = f"Patient(id = {self.id}, temperature = {self.temperature}, pulse = {self.pulse}, oxi = {self.oxi}, weight = {self.weight}, gluco = {self.gluco})"
        return rep

db.create_all()

patient_fields = {
    'id': fields.Integer,
    'temperature': fields.Float,
    'pulse': fields.Float,
    'oxi': fields.Float,
    'weight': fields.Float,
    'gluco': fields.Float
}

put_args = reqparse.RequestParser(bundle_errors=True)
put_args.add_argument('temperature', type=float, help='Invalid Temperature')
put_args.add_argument('pulse', type=float, help='Invalid Pulse')
put_args.add_argument('oxi',type=float, help='Invalid Oximeter')
put_args.add_argument('weight',type=float, help='Invalid Weight')
put_args.add_argument('gluco',type=float, help='Invalid Glucometer')

# resource to CRUD a single patient
class PatientResource(Resource):
    # Create/Update
    # breaks if you pass no readings
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
            return Response(status = 201)
        else:
            updated_readings = {}
            for key in args.keys():
                val = args[key]
                if val is not None:
                    updated_readings[key] = val
            db.session.query(PatientModel).filter(PatientModel.id == patientID).update(updated_readings) 
            db.session.commit()
            print(type(patient))
            return Response(status = 204)
    # Read
    @marshal_with(patient_fields)
    def get(self,patientID):
        patients = PatientModel.query.get_or_404(patientID)
        return patients, 200
    # Delete
    @marshal_with(patient_fields)
    def delete(self,patientID):
        patient = PatientModel.query.get_or_404(patientID)
        db.session.delete(patient)
        db.session.commit()
        return Response(status = 204)

#resource to CRUD the entire database of patients
class PatientsResource(Resource):
    # read
    @marshal_with(patient_fields)
    def get(self):
        patients = PatientModel.query.all()
        return patients, 200
    # delete
    @marshal_with(patient_fields)
    def delete(self):
        patients = PatientModel.query.all()
        for patient in patients:
            db.session.delete(patient)
        db.session.commit()
        return Response(status = 204)
        
api.add_resource(PatientResource,'/patients/<int:patientID>')
api.add_resource(PatientsResource,'/patients/')

if __name__ == '__main__':
    application.run(debug=True)