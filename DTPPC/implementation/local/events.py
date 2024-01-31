import json
from typing import List
import pandas as pd
from time import sleep
import asyncio

class EventCreator:
    def __init__(self,input_file:str,output_file:str=''):
        self.old = None
        self.output_file = output_file
        self.log = list()
        self.input_file = input_file
        '''
        with open('config.json') as f:
            self.input_path = json.load(f)['input_path']
        '''
    def events(self)->List[str]:
        e = []
        new = pd.read_excel(self.input_file,sheet_name='tblOrderPos') 
        if self.old is None:
            self.old = new.copy(deep=True)
            e.append('startUnscheduled')
            e.append('start')
            return e
        if len(new) != len(self.old):
            e.append('arrival')
        df=pd.concat([self.old,new]).drop_duplicates(keep=False).fillna(0).reset_index()
        if len(df) > 0:
            different_columns = df.loc[0].ne(df.loc[1])
            diff_cols = different_columns[different_columns].index.tolist()
            self.old = new
            if 'End' in diff_cols:
                e.append('completion')
                e.append('new')
            elif 'Start' in diff_cols:
                pass
        self.old = new.copy(deep=True)
        return e
    def process(self)->None:
        events = self.events()
        for event in events:
            print(pd.Timestamp.now(),event)
            self.log.append([pd.Timestamp.now(),event])
        if self.output_file is not None:
            with open(self.output_file,'w') as f:
                json.dump(self.log,f)
    def run(self,timeout):
        self.process()
        sleep(timeout)
    async def run_async(self,timeout):
        self.process()
        await asyncio.sleep(timeout)
        
if __name__ == '__main__':
    log = list()
    el = EventCreator()
    #temp
    el.old = pd.read_excel(el.input_path+'/MESb old.xlsx',sheet_name='tblOrderPos') 
    #
    el.run(10)
    while True:
        events = el.events()
        for event in events:
            print(pd.Timestamp.now(),event)
            log.append([pd.Timestamp.now(),event])
        sleep(1)
    
