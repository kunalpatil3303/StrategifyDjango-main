from .utils import *
from .models import *


def saveOrder(generateRandomUID,userdata,symbol,price,transaction_type,status,condition):
	Orders.objects.create(
		orderid = generateRandomUID,
		username = userdata,
		scrip = str(symbol),
		price = str(price),
		date = todayDate(),
		time = todayTime(),
		transaction_type = transaction_type,
		message = str(status),
		condition = str(condition),
		)