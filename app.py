from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Person(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  Name = db.Column(db.String(80), unique=True, nullable=False)
  Surname = db.Column(db.String(120), unique=True, nullable=False)

  def __init__(self, Name, Surname):
    self.Name = Name
    self.Surname = Surname

db.create_all()

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
  item = Person.query.get(id)
  del item.__dict__['_sa_instance_state']
  return jsonify(item.__dict__)

@app.route('/items', methods=['GET'])
def get_items():
  items = []
  for item in db.session.query(Person).all():
    del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
  return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():
  body = request.get_json()
  db.session.add(Person(body['Name'], body['Surname']))
  db.session.commit()
  return "item created"

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
  body = request.get_json()
  db.session.query(Person).filter_by(id=id).update(
    dict(Name=body['Name'], Surname=body['Surname']))
  db.session.commit()
  return "item updated"

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
  db.session.query(Person).filter_by(id=id).delete()
  db.session.commit()
  return "item deleted"