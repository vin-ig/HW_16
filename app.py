from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
	"""Модель пользователя"""
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	age = db.Column(db.Integer)
	email = db.Column(db.String(40))
	role = db.Column(db.String(20))
	phone = db.Column(db.String(20))


class Order(db.Model):
	"""Модель заказа"""
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=True)
	description = db.Column(db.String(200))
	start_date = db.Column(db.String(15))
	end_date = db.Column(db.String(15))
	address = db.Column(db.String(50))
	price = db.Column(db.Integer)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
	"""Модель предложения"""
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

# Заполняем таблицы
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
			start_date=order.get('start_date'),
			end_date=order.get('end_date'),
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
	"""Вывод и добавление пользователей"""
	if request.method == 'GET':
		result = []
		for user in db.session.query(User).all():
			result.append(response_user(user))
		return jsonify(result)

	elif request.method == 'POST':
		user = request.json
		allowed_keys = {'age', 'email', 'first_name', 'last_name', 'phone', 'role'}
		if check_keys(user, allowed_keys):
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
			return 'Новый пользователь успешно добавлен в базу!\n' \
					f'{json.dumps(response_user(new_user), indent=2, ensure_ascii=False)}'
		else:
			return 'В вводимых данных присутствуют неверные ключи'


@app.route('/users/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(id):
	"""Вывод, изменение, удаление пользователя"""
	user = db.session.query(User).get(id)
	if not user:
		return 'В БД нет объекта с таким ID'

	if request.method == 'GET':
		return jsonify(response_user(user))

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
		return 'Данные пользователя успешно обновлены!\n' \
				f'{json.dumps(response_user(user), indent=2, ensure_ascii=False)}'

	elif request.method == 'DELETE':
		db.session.delete(user)
		db.session.commit()
		return 'Пользователь успешно удален из базы!\n' \
				f'{json.dumps(response_user(user), indent=2, ensure_ascii=False)}'


@app.route('/orders/', methods=['GET', 'POST'])
def orders():
	"""Вывод и добавление заказов"""
	if request.method == 'GET':
		result = []
		for order in db.session.query(Order).all():
			result.append(response_order(order))
		return jsonify(result)

	elif request.method == 'POST':
		order = request.json
		allowed_keys = {'name', 'description', 'start_date', 'end_date', 'address', 'price', 'customer_id', 'executor_id'}
		if check_keys(order, allowed_keys):
			new_order = Order(
				name=order.get('name'),
				description=order.get('description'),
				start_date=order.get('start_date'),
				end_date=order.get('end_date'),
				address=order.get('address'),
				price=order.get('price'),
				customer_id=order.get('customer_id'),
				executor_id=order.get('executor_id')
			)
			with db.session.begin():
				db.session.add(new_order)
			return 'Новый заказ успешно добавлен в базу!\n' \
					f'{json.dumps(response_order(new_order), indent=2, ensure_ascii=False)}'
		else:
			return 'В вводимых данных присутствуют неверные ключи'


@app.route('/orders/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(id):
	"""Вывод, изменение, удаление заказов"""
	order = db.session.query(Order).get(id)
	if not order:
		return 'В БД нет объекта с таким ID'

	if request.method == 'GET':
		return jsonify(response_order(order))

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
		return 'Данные заказа успешно обновлены!\n' \
		        f'{json.dumps(response_order(order), indent=2, ensure_ascii=False)}'

	elif request.method == 'DELETE':
		db.session.delete(order)
		db.session.commit()
		return 'Заказ успешно удален из базы!\n' \
				f'{json.dumps(response_order(order), indent=2, ensure_ascii=False)}'


@app.route('/offers/', methods=['GET', 'POST'])
def offers():
	"""Вывод и добавление предложений"""
	if request.method == 'GET':
		result = []
		for offer in db.session.query(Offer).all():
			result.append(response_offer(offer))
		return jsonify(result)

	elif request.method == 'POST':
		offer = request.json
		allowed_keys = {'order_id', 'executor_id'}
		if check_keys(offer, allowed_keys):
			new_offer = Offer(
				order_id=offer.get('order_id'),
				executor_id=offer.get('executor_id')
			)
			with db.session.begin():
				db.session.add(new_offer)
			return 'Новое предложение успешно добавлено в базу!\n' \
					f'{json.dumps(response_offer(new_offer), indent=2, ensure_ascii=False)}'
		else:
			return 'В вводимых данных присутствуют неверные ключи'


@app.route('/offers/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(id):
	"""Вывод, изменение, удаление предложений"""
	offer = db.session.query(Offer).get(id)
	if not offer:
		return 'В БД нет объекта с таким ID'

	if request.method == 'GET':
		return jsonify(response_offer(offer))

	elif request.method == 'PUT':
		update = request.json

		offer.order_id = update.get('order_id', offer.order_id)
		offer.executor_id = update.get('executor_id', offer.executor_id)

		db.session.add(offer)
		db.session.commit()
		return 'Данные предложения успешно обновлены!\n' \
				f'{json.dumps(response_offer(offer), indent=2, ensure_ascii=False)}'

	elif request.method == 'DELETE':
		db.session.delete(offer)
		db.session.commit()
		return 'Предложение успешно удалено из базы!\n' \
				f'{json.dumps(response_offer(offer), indent=2, ensure_ascii=False)}'


if __name__ == '__main__':
	app.run()
