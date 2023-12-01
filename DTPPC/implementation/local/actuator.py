# define communicator of dvs to other machine
# define high-level actuator translating dvs into MES input
from typing import List
from DTPPC.implementation.local.dbConnect import DBConnection
import pyodbc
import pandas as pd
from DTPPC.implementation.local.planned_orders import planned_orders_simplified

class Actuator(DBConnection):
    def __init__(self):
        super().__init__(output_file='', tbls=[])
    def act(self,dvs:dict) -> None:
        if "sequence" in dvs.keys():
            self.sort(dvs["sequence"])
        if "admission" in dvs.keys():
            self.release(dvs["admission"])
    def new_dict(self,dv:dict)->dict:
        new_dv = dict()
        for key, value in dv.items():
            keys = key.split('-')  # Split the key by '-'
            new_dv[int(keys[0]), int(keys[1])] = value
        return new_dv
    def sort(self,dv) -> None:
        dv = self.new_dict(dv)
        min_ono, min_opos = min(dv, key=dv.get)
        query = f"SELECT PlanedStart FROM tblOrderPos WHERE ONo = {min_ono} AND OPos = {min_opos}"
        self.cur.execute(query)
        min_planned_start = self.cur.fetchone()[0].strftime('%Y-%m-%d %H:%M:%S')
        # debug
        query = f"SELECT PlanedStart FROM tblOrderPos"
        self.cur.execute(query)
        print(self.cur.fetchall())
        for key in dv:
            ono, opos = key
            seconds_to_add = dv[key]
            update_query = f"UPDATE tblOrderPos SET PlanedStart = DateAdd('s', {seconds_to_add}, #{min_planned_start}#) WHERE (ONo = ? AND OPos = ?)"
            self.cur.execute(update_query, (ono, opos))
            self.conn.commit()  # Commit changes to the database
        #debug
        query = f"SELECT PlanedStart FROM tblOrderPos"
        self.cur.execute(query)
        print(self.cur.fetchall())
        self.disconnect()
    def release(self,dv):
        # dv = {"6629-1":True,"6630-1":True}
        dv = self.new_dict(dv)
        # debug
        query = f"SELECT Enabled FROM tblOrder"
        self.cur.execute(query)
        print(self.cur.fetchall())
        for key in dv:
            ono, opos = key
            is_enabled = dv[key]
            update_query = f"UPDATE tblOrder SET Enabled = {is_enabled} WHERE ONo = ?"
            self.cur.execute(update_query, ono)
            self.conn.commit()  # Commit changes to the database
        #debug
        query = f"SELECT Enabled FROM tblOrder"
        self.cur.execute(query)
        print(self.cur.fetchall())
        self.disconnect()
    def old_sort(self, dv) -> None:
        self.connect()
        df = self.process()['tblOrderPos']
        # i connect to a ms access db using pyodbc and self.conn, self.cur is cursor; now i need to get data from a table and update them according to some dataframe (dv)


        # debug
        # dv = {"6618-1":1,"6619-1":2}
        # df = pd.read_excel("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx",sheet_name="tblOrderPos")
        dv = self.new_dict(dv)

        df_active = df.loc[~df['Start'].isna()]
        df_inactive = df.loc[df['Start'].isna()]

        df_inactive['sorting_values'] = df_inactive.apply(lambda row:dv.get((row['ONo'], row['OPos']), 0),axis=1)
        df_inactive.sort_values('sorting_values').drop('sorting_values', axis=1, inplace=True)

        df = pd.concat([df_active,df_inactive],ignore_index=True)
        self.write(df,"tblOrderPos")
        self.disconnect()
    def old_release(self, dv) -> None:
        self.connect()
        df = self.process()['tblOrder']
        # debug
        # dv = {"6618-1":True,"6619-1":False}
        # df = pd.read_excel("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx",sheet_name="tblOrder")

        df_active = df.loc[~df['Start'].isna()]
        df_inactive = df.loc[df['Start'].isna()]

        dv = self.new_dict(dv)
        dv =  {key: value for d in [{key[0]:dv[key]} for key in dv.keys()] for key, value in d.items()}

        df_inactive["Enable"] = df_inactive.apply(lambda row:dv.get((row["ONo"],1)),axis=1)

        df = pd.concat([df_active,df_inactive],ignore_index=True)
        self.write(df,"tblOrder")
        self.disconnect()
    def write(self,df:pd.DataFrame,table_name:str):
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

if __name__ == '__main__':
    class Actuator(Actuator):
        def connect(self):
            self.conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=D:/FestoMES.accdb;")
            self.cur = self.conn.cursor()
    a = Actuator()
    a.connect()
    a.release("")
