from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from datetime import *
import json

Base = declarative_base()

class db_manager(object):
	def __init__(self):

		engine = create_engine('sqlite:///:memory:', echo=False)
		Session = sessionmaker(bind=engine)
		self.session = Session()
		Base.metadata.create_all(engine)

	def add(self, agent_name, agent_data):
		"""adds to session a new entry of agent_name and agent_data
			commits the changes to the session"""
		self.session.add(AgentData(name=agent_name, date_time=datetime.now(), data=str(agent_data)))
		self.session.commit()

	def get_data(self, agent_name, begining_date):
		"""retrieved the data for a specific agent and starting with a specific date_time
			agent_name is a string specifying the agents name
			begining_date is a datetime object specifying the starting date to retreive the data"""
		data=[]
		result = self.session.query(AgentData.data).filter_by(name=agent_name).filter(AgentData.date_time >= begining_date).all()
		for r in result:
			data+=[json.loads(r[0].replace("'",'"'))]
		return data


class AgentData(Base):
	"""the model used for AgentsData table"""
	__tablename__ = "AgentsData"

	id=Column(Integer, primary_key=True)
	name=Column(String)
	date_time=Column(DateTime)
	data=Column(String)

	def __repr__(self):
			return "{name:'%s', date_time:'%s', data:'%s'}" % (self.name, self.date_time, self.data)

