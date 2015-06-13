import model
import datetime
import time

class test_model(object):
	def __init__(self):
		self.man = model.db_manager()

	def test_all(self):
		self.test_getdata_existingvalues()
		self.test_addgetdata_laterdate()
		self.test_addgetdata_emptydata()
		self.test_getdata_unexistingagent()

	def test_getdata_existingvalues(self):
		self.man.add("AgentTest1", {'data':'excluded'})
		time.sleep(1)
		
		d = datetime.datetime.now()
		self.man.add("AgentTest1", {'data':'included'})

		result = self.man.get_data("AgentTest1", d)

		try:
			for r in result:
				if r['data'] == 'included':
					print "test_getdata_existingvalues suceed"
				else :
					print "test failed: data = " + str(r['data'])
		except Exception:
			print "test met and exception"

	def test_addgetdata_emptydata(self):
		d = datetime.datetime.now()
		time.sleep(1)
		self.man.add("AgentTest2", {})
		result = self.man.get_data("AgentTest2", d)
		if result[0] == {}:
			print "test_adddata_emptystring suceed"
		else:
			print" test_adddata_emptystring failed, received:" + str(r)

	def test_addgetdata_laterdate(self):
		self.man.add("AgentTest3", {"data" : "late"})

		time.sleep(1)
		d = datetime.datetime.now()
		result = self.man.get_data("AgentTest3", d)
		if result == []:
			print "test_addgetdata_laterdate suceed"
		else:
			print "test_addgetdata_laterdate failed: result=" + str(result)

	def test_getdata_unexistingagent(self):
		d = datetime.datetime.now()
		result = self.man.get_data("UnexistingAgent",d)
		if result == []:
			print "test_getdata_unexistingagent suceed"
		else:
			print "test_getdata_unexistingagent failed: result="+str(result)