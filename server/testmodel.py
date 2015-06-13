import model
import datetime

class test_model(object):
	def __init__(self):
		self.man = model.db_manager()

	def test_getdata_existingvalues(self):
		self.man.add("AgentTest1", {'data':'excluded'})

		d = datetime.datetime.now()

		self.man.add("AgentTest1", {'data':'included'})

		result = self.man.get_data("AgentTest1", d)

		try:
			for r in result:
				if r['data'] == 'included':
					print "test suceed"
				else :
					print "test failed: data = " + str(r['data'])
		except Exception:
			print "test met and exception"