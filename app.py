from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import prettytable

app = Flask(__name__)
app.config['DEGUG'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'user'
	pass


class Offer(db.Model):
	__tablename__ = 'offer'
	pass


class Order(db.Model):
	__tablename__ = 'order'
	pass


@app.route('/')
def index():
	pass












if __name__ == '__main__':
	app.run()