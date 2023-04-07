# import config
# import json
# from flask import Flask
# from flask import render_template, request
# from ks_api_client import ks_api
#
# app = Flask(__name__)
#
#
# client = ks_api.KSTradeApi(access_token="2042d3ae-3eca-3a6e-823a-0cc63fa8574d", userid="TS01061986",
#                            consumer_key="oblkMRyEpbSam9fxb2j5XEYGmE8a", ip="127.0.0.1", app_id="1")
#
# client.login(password="ya@Mi786")
#
# client.session_2fa(access_code="7354")
#
# @app.route('/')
# def dashboard():
#     orders = client.order_report();
#     return render_template('dashboard.html', kotak_orders=orders)
#
#
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     webhook_message = json.loads(request.data)
#
#     print(webhook_message)
#
#     if webhook_message['passphrase'] != "aj$Ta786":
#         return {
#             'code': 'error',
#             'message': 'nice try buddy'
#         }
#
#     price = webhook_message['strategy']['order_price']
#     # quantity = webhook_message['strategy']['order_contracts']
#
#     quantity = 1
#     symbol = webhook_message['ticker']
#     side = webhook_message['strategy']['order_action']
#
#     if side == "BUY":
#         try:
#             # Place a Fixed Symbol Order
#             # If side Is Buy then Place Buy Order
#             client.place_order(order_type="N", instrument_token=symbol, transaction_type="BUY", quantity=quantity,
#                                price=0,
#                                disclosed_quantity=0, trigger_price=0,
#                                validity="GFD", variety="REGULAR", tag="string")
#
#             print("Order Placed ! ", symbol, quantity, side)
#         except Exception as e:
#             print("Exception when calling OrderApi->place_order: %s\n" % e)
#         return webhook_message
#     else:
#
#         try:
#             # Place a Fixed Symbol Order
#             # If side Is Buy then Place Buy Order
#             client.place_order(order_type="N", instrument_token=symbol, transaction_type="SELL", quantity=quantity,
#                                price=0,
#                                disclosed_quantity=0, trigger_price=0,
#                                validity="GFD", variety="REGULAR", tag="string")
#
#             print("Order Placed ! ", symbol, quantity, side)
#         except Exception as e:
#             print("Exception when calling OrderApi->place_order: %s\n" % e)
#         return webhook_message
#






from ks_api_client import ks_api

URL = ""
class Kotak():
	global URL
	def __init__(self, access_token, userid, consumer_key, app_id, password):
		self.access_token = access_token
		self.userid = userid
		self.consumer_key = consumer_key
		self.app_id = app_id
		self.password = password
		self.client = None

	def configure(self):
		self.client = ks_api.KSTradeApi(access_token=self.access_token, userid=self.userid,
												consumer_key=self.consumer_key, ip="127.0.0.1", app_id="APP")
		self.client.login(password=self.password)

	def session_login(self,acess_code):
		self.client.session_2fa(access_code=acess_code)


	def place_order(self,order_type,instrument_token,transaction_type,quantity,price,disclosed_quantity,trigger_price,validity,variety,tag):
		print("Client Info: ",self.client)
		self.client.place_order(order_type=order_type,instrument_token=instrument_token,transaction_type=transaction_type,
				quantity=quantity,price=price,disclosed_quantity=disclosed_quantity,
				trigger_price=trigger_price,validity=validity,variety=variety,tag=tag)
		print("BUY Order Placed ! ", instrument_token, quantity, transaction_type)

	def trade_report(self):
		print("Order Report: ")
		report = self.client.order_report()
		print(report)

	def trade_report_order(self,orderid):
		print("Order Report Id: ",orderid)
		report = self.client.order_report(order_id = orderid)
		print(report)

	def get_quote(self,token):
		try:
			print(self.client.quote(instrument_token = token))
		except Exception as e:
			print("Get Quote Exception: ",str(e))




