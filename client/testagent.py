from agent import *
from mock import *
from datetime import *

class test_agent(object):

	def test_all(self):
		self.test_printstatistics_callsonconnector()


	def test_printstatistics_callsonconnector(self):
		agent = Agent("name")
		agent.connector = Mock()
		d = datetime.now()
		agent.begining_date = d
		agent.print_statistics()

		agent.connector.request_data.assert_called_once_with("name", d)
		agent.connector.get_last_message.assert_called_once_with()