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
    sender_id = db.Column(db.Integer,nullable=False)
    recipient_id = db.Column(db.Integer,nullable=False)
    content = db.Column(db.String,nullable=False)
    time_stamp = db.Column(db.Float,nullable=False)       
    def __repr__(self):
        rep = f'\n"{self.content}"\nFROM: {self.sender_id} TO: {self.recipient_id} ON: {time.asctime(time.localtime(self.time_stamp))}\n'
        return rep

db.create_all()

msg_fields = {
    'id': fields.Integer,
    'sender_id': fields.Integer,
    'recipient_id': fields.Integer,
    'content': fields.String,
    'time_stamp': fields.Float
}

post_args = reqparse.RequestParser(bundle_errors=True)
post_args.add_argument('sender_id', type=int, help='Invalid sender ID')
post_args.add_argument('recipient_id',type=int, help='Invalid recipient ID')
post_args.add_argument('content',type=str, help='Invalid Content')

get_args = reqparse.RequestParser(bundle_errors=True)
get_args.add_argument('sender_id', type=int, help='Invalid sender ID')
get_args.add_argument('recipient_id',type=int, help='Invalid recipient ID')
get_args.add_argument('user A',type=int, help='Invalid "user A"')
get_args.add_argument('user B',type=int, help='Invalid "user B"')


class MessagesResource(Resource):
    # Create new msg
    @marshal_with(msg_fields)
    def post(self):
        args = post_args.parse_args()
        msg = MessageModel(
            sender_id = args['sender_id'],
            recipient_id = args['recipient_id'],
            content = args['content'],
            time_stamp = time.time()
        )
        db.session.add(msg)
        db.session.flush()
        db.session.commit()
        return 201
    # Read msgs/conversation
    @marshal_with(msg_fields)
    def get(self):
        args = get_args.parse_args()
        # if defined, query conversation between user A and user B
        if args['user A'] is not None and args['user B'] is not None:
            queryA = MessageModel.query.filter(MessageModel.sender_id == args['user A']).filter(MessageModel.recipient_id == args['user B'])
            queryB = MessageModel.query.filter(MessageModel.sender_id == args['user B']).filter(MessageModel.recipient_id == args['user A'])
            queryAB = queryA.union(queryB)
            msgs = queryAB.all()
        # else, query based on sender_id and/or recipient_id
        elif args['sender_id'] is None and args['recipient_id'] is None:
            abort(400, 'please define either (a) "user A" and "user B" to query a conversation \
                or (b) sender_id and/or recipient_id to query based on sender and/or recipient')
        elif args['sender_id'] is not None and args['recipient_id'] is None:
            msgs = MessageModel.query.filter(MessageModel.sender_id == args['sender_id']).all()
        elif args['sender_id'] is None and args['recipient_id'] is not None:
            msgs = MessageModel.query.filter(MessageModel.recipient_id == args['recipient_id']).all()
        elif args['sender_id'] is not None and args['recipient_id'] is not None:
            msgs = MessageModel.query.filter(MessageModel.sender_id == args['sender_id']).filter(MessageModel.recipient_id == args['recipient_id']).all()
        print(msgs)
        return msgs, 200
    # Delete all msgs
    @marshal_with(msg_fields)
    def delete(self):
        db.session.query(MessageModel).delete()
        db.session.commit()
        return 204
    
api.add_resource(MessagesResource,'/messages/')

if __name__ == '__main__':
    application.run(debug=True)