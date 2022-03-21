"""
TODO:
-marshal output using marshmallow
-split into application.py and APIS.py
-https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.TIMESTAMP
-complete delete method
"""


from flask import Flask, abort
from flask_restful import Api,Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import time

application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(application)

class MessageModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sender_id = db.Column(db.String,nullable=False)
    recipient_id = db.Column(db.String,nullable=False)
    content = db.Column(db.String,nullable=False)
    time_stamp = db.Column(db.Float,nullable=False)       
    def __repr__(self):
        rep = f'{time.asctime(time.localtime(self.time_stamp))}\nSender ID: {self.sender_id}\nRecipient ID: {self.recipient_id}\nContent: "{self.content}"'
        return rep

db.create_all()

msg_fields = {
    'id': fields.Integer,
    'sender_id': fields.Integer,
    'recipient_id': fields.Integer,
    'content': fields.String,
    'time_stamp': fields.Float
}

request_parser = reqparse.RequestParser(bundle_errors=True)
# request_parser.add_argument('id', type=int, help='Invalid ID')
request_parser.add_argument('sender_id', type=str, help='Invalid sender_id')
request_parser.add_argument('recipient_id',type=str, help='Invalid recipient_id')
request_parser.add_argument('content',type=str, help='Invalid Content')

class MessagesResource(Resource):
    # Create/Update
    @marshal_with(msg_fields)
    def post(self):
        args = request_parser.parse_args()
        msg = MessageModel(
            sender_id = args['sender_id'],
            recipient_id = args['recipient_id'],
            content = args['content'],
            time_stamp = time.time()
        )
        db.session.add(msg)
        db.session.flush()
        db.session.commit()
        return msg, 201
    # Read
    @marshal_with(msg_fields)
    def get(self):
        args = request_parser.parse_args()
        # keyphrase = '%' + str(args['content']) + '%'
        if args['sender_id'] is None and args['recipient_id'] is None:
            abort(400, 'sender_id and/or recipient_id required')
        elif args['sender_id'] is not None and args['recipient_id'] is None:
            msgs = MessageModel.query.filter(MessageModel.sender_id == args['sender_id']).all()
        elif args['sender_id'] is None and args['recipient_id'] is not None:
            msgs = MessageModel.query.filter(MessageModel.sender_id == args['sender_id']).all()
        elif args['sender_id'] is not None and args['recipient_id'] is not None:
            msgs = MessageModel.query.filter(MessageModel.sender_id == args['sender_id']).filter(MessageModel.recipient_id == args['recipient_id']).all()
        return msgs, 200
    # Delete
    # not yet functional
    @marshal_with(msg_fields)
    def delete(self):
        response = self.get()
        print(response)
        return response
    

api.add_resource(MessagesResource,'/messages/')

if __name__ == '__main__':
    application.run(debug=True)