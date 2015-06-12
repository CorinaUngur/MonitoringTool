import pika
import json
import uuid

class Connector(object):
	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
		self.channel = self.connection.channel()

		self.callback_queue = self.channel.queue_declare(exclusive=True).method.queue

		self.channel.queue_declare(queue='data', durable=False)
		self.channel.queue_declare(queue='request', durable=False)

		self.channel.basic_consume(self.__on_request_response__, no_ack=True, queue=self.callback_queue)

	def send_data(self, agent_name, data):
		message = [agent_name, data]
		try:
			msg = json.dumps(message)
		except ValueError:
			msg = '["wrong_message"]'
		self.channel.basic_publish(exchange='',
					 routing_key='data', 
					 properties=pika.BasicProperties(content_type="application/json", delivery_mode = 1), 
					 body=json.dumps(message))

	def request_data(self, agent_name, begining_date):
		message = [agent_name, begining_date]
		self.response = None

		corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='request',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue,
									correlation_id = corr_id,
									content_type="application/json",
									delivery_mode = 1
									),
									body=json.dumps(message))

		while self.response is None:
			self.connection.process_data_events()

	def __on_request_response__(self, ch, method, props, body):
		try:
			self.last_message = json.loads(body)
		except ValueError:
			print 'encountered an error while decoding the message'

		self.response = 'received'

	def get_last_message(self):
		return self.last_message

