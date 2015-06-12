from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from datetime import *
import json

Base = declarative_base()

class db_manager(object):
	def __init__(self):

		engine = create_engine('sqlite:///:memory:', echo=True)
		Session = sessionmaker(bind=engine)
		self.session = Session()
		Base.metadata.create_all(engine)

	def add(self, agent_name, agent_data):
		self.session.add(AgentData(name=agent_name, date_time=datetime.now(), data=str(agent_data)))
		self.session.commit()

	def get_data(self, agent_name, begining_date):
		data=[]
		result = self.session.query(AgentData.data).filter_by(name=agent_name).filter(AgentData.date_time >= begining_date).all()
		for r in result:
			data+=[r[0]]
		return data


class AgentData(Base):
	__tablename__ = "AgentsData"

	id=Column(Integer, primary_key=True)
	name=Column(String)
	date_time=Column(DateTime)
	data=Column(String)

	def __repr__(self):
			return "{name:'%s', date_time:'%s', data:'%s'}" % (self.name, self.date_time, self.data)

