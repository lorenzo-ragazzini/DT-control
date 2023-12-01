import pyodbc
import pandas as pd
from time import sleep
import asyncio

class DBConnection:
	def __init__(self):
		self.conn = None
		self.cur = None
	def connect(self):
		self.conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=C:/MES4/FestoMES.accdb;")
		self.cur = self.conn.cursor()
	def disconnect(self):
		self.cur.close()
		self.conn.close()

class DBReader(DBConnection):
	def __init__(self,output_file:str,tbls=["tblStepDef","tblStep","tblOrderPos","tblOrder"]):
		self.tbls = tbls
		self.path_to_file = output_file
		super().__init__()
	def run(self,timeout):
		try:
			while True:
				self.connect()
				dfs = self.process()
				self.save(dfs)
				self.disconnect()
				sleep(timeout)
		except Exception: #disconnect in case of error
			print(Exception)
		try:
			self.disconnect()
		except:
			pass
	async def run_async(self,timeout):
		try:
			while True:
				self.connect()
				dfs = self.process()
				self.save(dfs)
				self.disconnect()
				await asyncio.sleep(timeout)
		except: #disconnect in case of error
			self.disconnect()
	def process(self):
		dfs = dict()
		for tbl in self.tbls:
			query = "SELECT * FROM "+tbl
			qry = self.cur.execute(query)
			df = pd.DataFrame(qry.fetchall())
			cols = pd.read_sql(query, self.conn).columns
			if df.size>0:
				df.columns=[0]
				df = df[0].apply(list).apply(pd.Series)
				df.columns = cols
			else:
				df = pd.DataFrame(qry.fetchall(),columns=cols)
			dfs[tbl] = df
		return dfs
	def save(self,dfs):
		with pd.ExcelWriter(self.path_to_file) as writer:
			for tbl in self.tbls:
				dfs[tbl].to_excel(writer, sheet_name=tbl, index=False)

if __name__ == '__main__':
	c=DBReader(tbls=["tblStepDef","tblStep","tblOrderPos"],path_to_file='MESb.xlsx')
	c.connect()
	if True:
		asyncio.run(c.run_async(timeout=5))
	else:
		c.run(timeout=5)

'''
if __name__ == '__main__':	
	#pyodbc.lowercase = False
	conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=C:/MES4/FestoMES.accdb;")
	cur = conn.cursor()
	#qry = cur.execute('select * from tblStep')
	#qry = cur.execute('select * from tblStepDef')
	#cur.execute('select * from tblOrderPos')

	dfs = dict()
	for tbl in ["tblStepDef","tblStep","tblOrderPos"]:
		query = "SELECT * FROM "+tbl
		qry = cur.execute(query)
		df = pd.DataFrame(qry.fetchall())
		cols = pd.read_sql(query, conn).columns
		if df.size>0:
			df.columns=[0]
			df = df[0].apply(list).apply(pd.Series)
			df.columns = cols
		else:
			df = pd.DataFrame(qry.fetchall(),columns=cols)
		dfs[tbl] = df
		#df.columns=pd.read_sql(query, conn).columns
		#df[0].to_list(), columns=pd.read_sql(query, conn).columns)
		#dfs[query] = pd.DataFrame(qry.fetchall().str.split(','),columns=)
	print(dfs)

	with pd.ExcelWriter("MESb.xlsx") as writer:
		for tbl in ["tblStepDef","tblStep","tblOrderPos"]:
			dfs[tbl].to_excel(writer, sheet_name=tbl, index=False)

	cur.close()
	conn.close()
	'''