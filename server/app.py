from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
        if request.method == 'GET':
            try:
                messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
                response = make_response(
                    messages,
                    200 
                )
            except: 
                response = make_response(
                {"ERROR" : "COULDN'T FIND MESSAGES"},
                404
                )
            return response
        elif request.method == 'POST':
            try:
                if request.headers.get("Content-Type") == 'application/json':
                    form_data = request.get_json()
                else: 
                    form_data = request.form
                new_message = Message(
                    body = form_data['body'],
                    username = form_data['username']
                )
                db.session.add(new_message)
                db.session.commit()

                response = make_response(
                    new_message.to_dict(), 
                    201
                )
            except Exception as e:
                response = make_response(
                    {"ERROR" : str(e)}, 
                    500
                )
            return response
@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    try:
        message = Message.query.filter(Message.id == id).first()
        if request.method == 'PATCH':
            try:
                if request.headers.get("Content-Type") == 'application/json':
                    form_data = request.get_json()
                else: 
                    form_data = request.form

                for attr in form_data:
                    setattr(message, attr, form_data[attr])
                db.session.commit()

                response = make_response(
                    message.to_dict(), 
                    200
                )

            except Exception as e:
                response = make_response(
                    {"ERROR" : str(e)}, 
                    500
                )
            return response
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response = make_response(
                {"SUCCESS" : "Message Deleted"},
                202
            )
    except: 
        response = make_response(
            {"ERROR" : "COULDN'T FIND MESSAGE"},
            404
        )
    return response


if __name__ == '__main__':
    app.run(port=5555)
