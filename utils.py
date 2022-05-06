import json


def load_json(path):
	"""Загружает данные из json-файла"""
	with open(path, encoding='utf-8') as file:
		return json.load(file)


def response_user(user):
	"""Выводит json с данными пользователя"""
	return {
		'age': user.age,
		'email': user.email,
		'first_name': user.first_name,
		'id': user.id,
		'last_name': user.last_name,
		'phone': user.phone,
		'role': user.role
	}


def response_order(order):
	"""Выводит json с данными заказа"""
	return {
		'id': order.id,
		'name': order.name,
		'description': order.description,
		'start_date': order.start_date,
		'end_date': order.end_date,
		'address': order.address,
		'price': order.price,
		'customer_id': order.customer_id,
		'executor_id': order.executor_id
		}


def response_offer(offer):
	"""Выводит json с данными предложения"""
	return {
		'id': offer.id,
		'order_id': offer.order_id,
		'executor_id': offer.executor_id
		}
