from flask import Flask
from models import db
from device_REST import device_api

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
application.register_blueprint(device_api)



@application.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    application.run(debug=True)