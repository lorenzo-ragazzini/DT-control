import json
import pandas as pd
from time import sleep
import asyncio
from dtInput import MessengerOnly

class EventCreator:
    def __init__(self,input_filename='MESb.xlsx',output_file=None):
        self.old = None
        self.input_filename = input_filename
        self.output_file = output_file
        self.log = list()
        with open('config.json') as f:
            self.input_path = json.load(f)['input_path']      
    def events(self):
        new = pd.read_excel(self.input_path+self.input_filename,sheet_name='tblOrderPos') 
        if self.old is None:
            self.old = new
            return []
        df=pd.concat([self.old,new]).drop_duplicates(keep=False).fillna(0).reset_index()
        if len(df) == 0:
            return []
        different_columns = df.loc[0].ne(df.loc[1])
        result = different_columns[different_columns].index.tolist()
        self.old = new
        return result
    def run(self,timeout):
        events = self.events()
        for event in events:
            print(pd.Timestamp.now(),event)
            self.log.append([pd.Timestamp.now(),event])
        if self.output_filename is not None:
            with open(self.input_path+'/'+self.output_filename,'w') as f:
                json.dump(self.log,f)
        sleep(timeout)

class EventCreatorMsg(EventCreator):
    def __init__(self,queue_name,input_filename='MESb.xlsx',output_file=None):
        self.msg = MessengerOnly(queue_name)
        super().__init__(input_filename,output_file)
    async def msgRun(self,timeout):
        events = self.events()
        for event in events:
            print(pd.Timestamp.now(),event)
            self.log.append([pd.Timestamp.now(),event])
            self.msg.send(event)

class EventListener:
    def __init__(self,queue_name):
        self.msg = MessengerOnly(queue_name)
        self.log = list()
        self.ctrl = None
    async def do(self):
        events = self.msg.receive()
        for event in events:
            self.ctrl.send(event)
        await asyncio.sleep(1)
        
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
    