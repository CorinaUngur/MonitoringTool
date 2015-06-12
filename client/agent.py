from wmi import *
from connector import *
from datetime import *
import time
import json

class Agent(object):

	def __init__(self, agent_name):
		self.name = agent_name
		self.w = WMI()
		self.connector = Connector()

	def start_sending(self, time_period=600, time_interval = 10):
		data = {}
		current_time = 0
		self.begining_date = datetime.now().strftime('%Y-%b-%d %I:%M:%S')

		while(current_time<=time_period):
			free_space = str(self.w.Win32_LogicalDisk()[0].FreeSpace)
			cpu_load = self.w.Win32_Processor()[0].LoadPercentage

			data['free_space'] = free_space
			data['cpu_load'] = cpu_load

			self.connector.send_data(self.name, data)

			time.sleep(time_interval)
			current_time += time_interval

	def print_statistics(self):
		self.connector.request_data(self.name, self.begining_date)
		message = self.connector.get_last_message()

		print 'cpu_load\t\tfree_space'
		for msg in message:
			m = json.loads(msg)
			print str(m['cpu_load'])+ '\t' + m['free_space']
