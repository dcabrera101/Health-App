from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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