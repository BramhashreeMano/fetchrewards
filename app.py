from flask import Flask, Response
from flask_restful import Resource, Api
from flask import jsonify
import json
import math
from flask import request
from datetime import datetime


import uuid
from re import sub
app = Flask(__name__)
api = Api(app)
data = []

db_stub = {}


def calculate_points(receipt_data):
	overall_points = 0
	# calculation logic
	# One point for every alphanumeric character in the retailer name.
	retailer_name = receipt_data.get('retailer', '')
	total_chars = sub(r'\W+', '', retailer_name)
	retailer_point = len(total_chars)
	overall_points += retailer_point
	# 50 points if the total is a round dollar amount with no cents
	bonus_for_no_cents = 50
	overall_bill_amount = 0.0
	for item in receipt_data.get('items', []):
		overall_bill_amount = overall_bill_amount + float(item['price'])
	overall_bill_amount = round(overall_bill_amount, 2)
	if overall_bill_amount.is_integer():
		overall_points += bonus_for_no_cents
	# 25 points if the total is a multiple of 0.25
	if overall_bill_amount > 0:
		cent_value = str(overall_bill_amount).split('.')[-1]
		if int(cent_value) % 25 == 0:
			overall_points += 25
	# 5 points for every two items on the receipt.
	overall_product_count = len(receipt_data.get('items', []))
	bonus_point_for_pairs = (overall_product_count // 2) * 5
	overall_points += bonus_point_for_pairs
	# If the trimmed length of the item description is a multiple of 3,
	# multiply the price by 0.2 and round up to the nearest integer.
	# The result is the number of points earned.
	description_bonus = 0
	for item in receipt_data.get('items', []):
		product_name = item['shortDescription'].strip()
		if len(product_name) % 3 == 0:
			description_bonus += math.ceil(float(item['price']) * 0.2)
	overall_points += description_bonus
	# 6 points if the day in the purchase date is odd.
	try:
		purchase_date = datetime.strptime(receipt_data['purchaseDate'], '%Y-%m-%d')
		if purchase_date.day % 2 != 0:
			overall_points += 6
	except Exception as e:
		print(str(e))
		pass
	# 10 points if the time of purchase is after 2:00pm and before 4:00pm.
	try:
		purchase_time = datetime.strptime(receipt_data['purchaseTime'], '%H:%M')
		start_time = datetime.strptime('14:00', '%H:%M')
		end_time = datetime.strptime('16:00', '%H:%M')
		if start_time < purchase_time < end_time:
			overall_points += 10
	except Exception as e:
		print(str(e))
		pass
	return overall_points


class ReceiptsProcessing(Resource):

	def post(self):
		# response object
		response = {}
		# fetching the request data
		receipt_info = request.json
		# calculating points
		calculated_points = calculate_points(receipt_info)
		# generating UUID
		request_id = str(uuid.uuid4())
		# setting in the response object
		response['id'] = request_id
		# stub for the db
		db_stub[request_id] = calculated_points
		return jsonify(response)


class ReceiptPoints(Resource):

	def get(self, id):
		response = {}
		if not db_stub.get(id):
			return Response(json.dumps({
				'status': 'Invalid Receipt ID'
			}), 404, headers={
				'Content-type': 'application/json'
			})
		response['points'] = db_stub[id]
		return jsonify(response)


api.add_resource(ReceiptPoints, '/receipts/<string:id>/points/', endpoint='points')
api.add_resource(ReceiptsProcessing, '/receipts/process')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
