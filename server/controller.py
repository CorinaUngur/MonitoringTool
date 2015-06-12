from pika import *
from model import db_manager
import json
from datetime import *

class Controller(object):

	def __init__(self):
		connection = BlockingConnection(ConnectionParameters(
		host='localhost'))

		self.channel = connection.channel()

		self.channel.queue_declare(queue='data', durable=False)
		self.channel.queue_declare(queue='request', durable=False)

		self.dbmanager = db_manager()

	def on_receive_data(self, ch, method, props, body):
		try:
			message = json.loads(body)
			agent_name = message[0]
			agent_data = json.dumps(message[1])

			self.dbmanager.add(agent_name, agent_data)
		except ValueError:
			print "received body is not a valid json"

	def on_receive_request(self, ch, method, props, body):
		try:
			message = json.loads(body)
			agent_name = message[0]
			begining_date = datetime.strptime(message[1],'%Y-%b-%d %I:%M:%S')
			entries = self.dbmanager.get_data(agent_name, begining_date)
			json_last_entries = json.dumps(entries)
			
		except ValueError:
			json_last_entries = "Error while decoding json"

		ch.basic_ack(delivery_tag = method.delivery_tag)
		ch.basic_publish(exchange='',
							routing_key=props.reply_to,
							properties=BasicProperties(correlation_id = \
													props.correlation_id,
													delivery_mode = 1),
							body=json_last_entries)


	def start(self):
		self.channel.basic_consume(self.on_receive_data, queue='data')
		self.channel.basic_consume(self.on_receive_request, queue='request')

		self.channel.start_consuming()