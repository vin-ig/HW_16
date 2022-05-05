from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import prettytable
from utils import *
from pprint import pprint
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
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
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=True)
	description = db.Column(db.String(200))
	start_date = db.Column(db.Date)
	end_date = db.Column(db.Date)
	address = db.Column(db.String(50))
	price = db.Column(db.Integer)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
	__tablename__ = 'offer'
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	order = db.relationship('Order')
	executor = db.relationship('User')


db.create_all()

users = load_json('users.json')
orders = load_json('orders.json')
offers = load_json('offers.json')

with db.session.begin():
	for user in users:
		db.session.add(User(
			age=user.get('age'),
			email=user.get('email'),
			first_name=user.get('first_name'),
			id=user.get('id'),
			last_name=user.get('last_name'),
			phone=user.get('phone'),
			role=user.get('role')
		))

	for order in orders:
		db.session.add(Order(
			id=order.get('id'),
			name=order.get('name'),
			description=order.get('description'),
			start_date=datetime.strptime(order.get('start_date'), '%m/%d/%Y').date(),
			end_date=datetime.strptime(order.get('end_date'), '%m/%d/%Y').date(),
			address=order.get('address'),
			price=order.get('price'),
			customer_id=order.get('customer_id'),
			executor_id=order.get('executor_id')
		))

	for offer in offers:
		db.session.add(Offer(
			id=offer.get('id'),
			order_id=offer.get('order_id'),
			executor_id=offer.get('executor_id')
		))


@app.route('/users/', methods=['GET', 'POST'])
def users():
	if request.method == 'GET':
		result = []
		for user in db.session.query(User).all():
			result.append({
				'age': user.age,
				'email': user.email,
				'first_name': user.first_name,
				'id': user.id,
				'last_name': user.last_name,
				'phone': user.phone,
				'role': user.role
				})
		return jsonify(result)

	elif request.method == 'POST':
		user = request.json
		new_user = User(
			age=user.get('age'),
			email=user.get('email'),
			first_name=user.get('first_name'),
			last_name=user.get('last_name'),
			phone=user.get('phone'),
			role=user.get('role')
		)
		with db.session.begin():
			db.session.add(new_user)
		return f'Новый пользователь по имени {new_user.first_name} {new_user.last_name} успешно добавлен в базу!'


@app.route('/users/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(id):
	user = db.session.query(User).get(id)

	if request.method == 'GET':
		return jsonify({
			'age': user.age,
			'email': user.email,
			'first_name': user.first_name,
			'id': user.id,
			'last_name': user.last_name,
			'phone': user.phone,
			'role': user.role
		})

	elif request.method == 'PUT':
		update = request.json

		user.age = update.get('age', user.age)
		user.email = update.get('email', user.email)
		user.first_name = update.get('first_name', user.first_name)
		user.last_name = update.get('last_name', user.last_name)
		user.phone = update.get('phone', user.phone)
		user.role = update.get('role', user.role)

		db.session.add(user)
		db.session.commit()
		return f'Данные пользователя {user.first_name} {user.last_name} с ID {user.id} успешно обновлены!'

	elif request.method == 'DELETE':
		db.session.delete(user)
		db.session.commit()
		return f'Пользователь {user.first_name} {user.last_name} с ID {user.id} успешно удален из базы!'


@app.route('/orders/', methods=['GET', 'POST'])
def orders():
	if request.method == 'GET':
		result = []
		for order in db.session.query(Order).all():
			result.append({
				'id': order.id,
				'name': order.name,
				'description': order.description,
				'start_date': order.start_date,
				'end_date': order.end_date,
				'address': order.address,
				'price': order.price,
				'customer_id': order.customer_id,
				'executor_id': order.executor_id
			})
		return jsonify(result)

	elif request.method == 'POST':
		order = request.json
		new_order = Order(
			id=order.get('id'),
			name=order.get('name'),
			description=order.get('description'),
			start_date=datetime.strptime(order.get('start_date'), '%m/%d/%Y').date(),
			end_date=datetime.strptime(order.get('end_date'), '%m/%d/%Y').date(),
			address=order.get('address'),
			price=order.get('price'),
			customer_id=order.get('customer_id'),
			executor_id=order.get('executor_id')
		)
		with db.session.begin():
			db.session.add(new_order)
		return f'Новый заказ "{new_order.name}" успешно добавлен в базу!'


@app.route('/orders/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(id):
	order = db.session.query(Order).get(id)

	if request.method == 'GET':
		return jsonify({
				'id': order.id,
				'name': order.name,
				'description': order.description,
				'start_date': order.start_date,
				'end_date': order.end_date,
				'address': order.address,
				'price': order.price,
				'customer_id': order.customer_id,
				'executor_id': order.executor_id
				})

	elif request.method == 'PUT':
		update = request.json

		order.name = update.get('name', order.name)
		order.description = update.get('description', order.description)
		order.start_date = update.get('start_date', order.start_date)
		order.end_date = update.get('end_date', order.end_date)
		order.address = update.get('address', order.address)
		order.price = update.get('price', order.price)
		order.customer_id = update.get('customer_id', order.customer_id)
		order.executor_id = update.get('executor_id', order.executor_id)

		db.session.add(order)
		db.session.commit()
		return f'Данные заказа "{order.name}" с ID {order.id} успешно обновлены!'

	elif request.method == 'DELETE':
		db.session.delete(order)
		db.session.commit()
		return f'Заказ "{order.name}" с ID {order.id} успешно удален из базы!'


@app.route('/offers/', methods=['GET', 'POST'])
def offers():
	if request.method == 'GET':
		result = []
		for offer in db.session.query(Offer).all():
			result.append({
				'id': offer.id,
				'order_id': offer.order_id,
				'executor_id': offer.executor_id
			})
		return jsonify(result)

	elif request.method == 'POST':
		offer = request.json
		new_offer = Offer(
			id=offer.get('id'),
			order_id=offer.get('order_id'),
			executor_id=offer.get('executor_id')
		)
		with db.session.begin():
			db.session.add(new_offer)
		return f'Новое предложение "{new_offer.name}" успешно добавлено в базу!'


@app.route('/offers/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(id):
	offer = db.session.query(Offer).get(id)

	if request.method == 'GET':
		return jsonify({
				'id': offer.id,
				'order_id': offer.order_id,
				'executor_id': offer.executor_id
				})

	elif request.method == 'PUT':
		update = request.json

		offer.id = update.get('id', offer.id)
		offer.order_id = update.get('order_id', offer.order_id)
		offer.executor_id = update.get('executor_id', offer.executor_id)

		db.session.add(offer)
		db.session.commit()
		return f'Данные предложения "{offer.name}" с ID {offer.id} успешно обновлены!'

	elif request.method == 'DELETE':
		db.session.delete(offer)
		db.session.commit()
		return f'Заказ "{offer.name}" с ID {offer.id} успешно удален из базы!'


def print_table():
	cursor = db.session.execute('SELECT * from user').cursor
	print(prettytable.from_db_cursor(cursor))

	cursor = db.session.execute('SELECT * from `order`').cursor
	print(prettytable.from_db_cursor(cursor))

	cursor = db.session.execute('SELECT * from offer').cursor
	print(prettytable.from_db_cursor(cursor))


# print_table()

if __name__ == '__main__':
	app.run()
