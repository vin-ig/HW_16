import json


def load_json(path):
	with open(path, encoding='utf-8') as file:
		return json.load(file)
