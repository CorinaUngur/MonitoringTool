from agent import *
from mock import *
from datetime import *

class test_agent(object):

	def test_all(self):
		self.test_printstatistics_callsonconnector()
#		self.test_senddata_callsonconnector()


	def test_printstatistics_callsonconnector(self):
		agent = Agent("name")
		agent.connector = Mock()
		d = datetime.now()
		agent.begining_date = d
		agent.print_statistics()

		agent.connector.request_data.assert_called_once_with("name", d)
		agent.connector.get_last_message.assert_called_once_with()

# 	def test_senddata_callsonconnector(self):
# 		agent = Agent("test2")
# 		agent.connector = Mock()
# 		freespace = 2345
# 		load = 99
# 		test = Test()
# 		test.LoadPercentage = freespace
# 		test.FreeSpace = load
# 		vect = [test]
# 		agent.w.Win32_LogicalDisk = MagicMock(vect)
# 		agent.w.Win32_Processor = MagicMock(vect)
# 		agent.send(1,1)
# 		data = {"cpu_load": load, "free_space":freespace}
# 		agent.connector.send_data.assert_called_with("test2", data)

# class Test(object):
# 	LoadPercentage = 10
# 	FreeSpace = 20