import pika
import json
import uuid

class Connector(object):
	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
		self.channel = self.connection.channel()

		self.callback_queue = self.channel.queue_declare(exclusive=True, auto_delete=True).method.queue

		self.channel.queue_declare(queue='data', durable=False, auto_delete=True)
		self.channel.queue_declare(queue='request', durable=False, auto_delete=True)

		self.channel.basic_consume(self.__on_request_response__, no_ack=True, queue=self.callback_queue)

	def send_data(self, agent_name, data):
		"""receives the name of the agent specified by agent_name and some data from this agent
			converts the agent_name and data to json and sends it to the controller
			agent_name is a string
			data can be in any conversible to json format"""
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
		"""sends a request to the controller for the data specific to the agent agent_name, newer then a specific begining_date
			agent_name is a string object
			begining_date is a datetime object"""

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
		"""process the data received after the request_data
			tries to convert the body which comes in a json format and save it in last_message field
			if does not suceed saves the original body received"""
		try:
			self.last_message=[]
			message = json.loads(body)
			for msg in message:
				self.last_message += [json.loads(msg)]
			
		except ValueError:
			print 'encountered an error while decoding the message'
			self.last_message = body

		self.response = 'received'

	def get_last_message(self):
		"""returns the last message received on a request response"""
		return self.last_message

