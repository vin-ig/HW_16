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
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	age = db.Column(db.Integer)
	email = db.Column(db.String(40))
	role = db.Column(db.String(20))
	phone = db.Column(db.String(20), unique=True, nullable=True)


class Order(db.Model):
	__tablename__ = 'orders'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=True)
	description = db.Column(db.String(200))
	start_date = db.Column(db.Date)
	end_date = db.Column(db.Date)
	address = db.Column(db.String(50))
	price = db.Column(db.Integer)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	customer = db.relationship('User')
	executor = db.relationship('User')


class Offer(db.Model):
	__tablename__ = 'offer'
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	order = db.relationship('Order')
	executor = db.relationship('User')


@app.route('/')
def index():
	pass


with db.session.begin():
	db.drop_all()
	db.create_all()

	cursor = db.session.execute("SELECT * from user").cursor
	print(prettytable.from_db_cursor(cursor))

	cursor = db.session.execute("SELECT * from orders").cursor
	print(prettytable.from_db_cursor(cursor))

	cursor = db.session.execute("SELECT * from offer").cursor
	print(prettytable.from_db_cursor(cursor))







exit()


if __name__ == '__main__':
	app.run()