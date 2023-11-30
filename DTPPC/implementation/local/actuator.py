# define communicator of dvs to other machine
# define high-level actuator translating dvs into MES input
from typing import List
from DTPPC.implementation.local.dbConnect import DBConnection
import pyodbc
import pandas as pd
from DTPPC.implementation.local.planned_orders import planned_orders_simplified

class Actuator(DBConnection):
    def act(self,dvs):
        pass
    def new_dict(self,dv:dict)->dict:
        new_dv = dict()
        for key, value in dv.items():
            keys = key.split('-')  # Split the key by '-'
            new_dv[int(keys[0]), int(keys[1])] = value
        return new_dv
    def sort(self):
        self.connect()
        df = self.process()['tblOrderPos']
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
    def release(self):
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
    a = Actuator('')
    a.sort()
