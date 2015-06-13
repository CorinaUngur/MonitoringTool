from agent import *
from mock import *
from datetime import *

class test_agent(object):

	def test_all(self):
		self.test_printstatistics_callsonconnector()
		self.test_senddata_callsonconnector()
		self.test_senddata_sendnothing()


	def test_printstatistics_callsonconnector(self):
		agent = Agent("name")
		agent.connector = Mock()
		d = datetime.now()
		agent.begining_date = d
		agent.print_statistics()

		agent.connector.request_data.assert_called_once_with("name", d)
		agent.connector.get_last_message.assert_called_once_with()

	def test_senddata_callsonconnector(self):
		agent = Agent("test2")
		agent.connector = Mock()
		freespace = 2345
		load = 99

		data = {"cpu_load": load, "free_space":freespace}
		agent.__get_current_data__ = Mock()
		agent.__get_current_data__.return_value = data

		agent.send_data(1,1)
		agent.connector.send_data.assert_called_with("test2", data)

	def test_senddata_sendnothing(self):
		agent = Agent('test3')

		agent.connector = Mock()

		agent.send_data(0,1)

		assert not agent.connector.send_data.called, "connector.send_data shoud have not been called"

