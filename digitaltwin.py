import os
import re
import time
import json
import numpy as np
import pandas as pd
from plantsim.plantsim import Plantsim
from plantsim.table import Table

class DigitalTwin():
    def __init__(self) -> None:
        with open('config.json') as f:
            paths = json.load(f)
            self.model_path = paths['model_path']
            self.output_path = paths['output_path']
            self.input_path = paths['input_path']
            self.output_filenames = ["FinishTimes.xlsx","TotEnergyConsumption.xlsx"]      
    def start(self):
        self.plantsim = Plantsim(version = '16.0', license_type='Student', trust_models=True)
        self.plantsim.load_model(self.model_path)
        self.plantsim.set_path_context('.Models.Model')
        self.plantsim.set_event_controller()
    def stop(self):
        self.plantsim.reset_simulation()
        self.plantsim.quit()
    def plantsim_run(self):
        if not hasattr(self,'plantsim'):
            self.start()
        for file in os.listdir(self.output_path):
            os.remove(self.output_path+'/'+file)
        self.plantsim.reset_simulation()
        self.plantsim.start_simulation()
        for filename in self.output_filenames:       
            while not os.path.exists(os.path.join(self.output_path, filename)):
                time.sleep(0.1)
        return
    def synchronize(self,taskResourceInformation:dict={}):
        if not taskResourceInformation:
            from controller.sync import planned_orders
            df = planned_orders()
        else:
            df = pd.DataFrame(taskResourceInformation)
            df.to_excel(fr"{self.input_path}\Order_Table.xlsx", index=False)
    def update(self,controlUpdate:dict):
        try:
            sequence = controlUpdate['executeSchedule']['sequence']
            pd.Series(sequence).to_excel(fr"{self.input_path}\Sequence.xlsx",index=False,header=True)
        except:
            pass
        try:
            CONWIP_value = controlUpdate['admission']['CONWIP_value']
            pd.Series(CONWIP_value).to_excel(fr"{self.input_path}\ConwipValue.xlsx",index=False,header=False)
        except:
            pass
    def simulate(self,request,write=False):
        # configuration=pd.DataFrame()
        # configuration['simLength'] = request['simLength']
        configuration=pd.DataFrame(request['input'],index=[0])
        configuration.to_excel(fr"{self.input_path}\Configuration.xlsx", index=False)
        results = dict()
        for ii in range(request['nrOfSimul']):
            self.plantsim_run()
            results[ii] = self.output_analysis(request)
        if not write:
            if len(results) == 1:
                results = results[0]
            return results
        else:
            with open('results.json', 'w') as f:
                json.dump(results, f)
            return
    def interface(self,taskResourceInformation:dict={},controlUpdate=None,request=None,write=False)->None:
        self.synchronize(taskResourceInformation)
        self.update(controlUpdate)
        return self.simulate(request)
    def output_analysis(self,request)->dict:
        self.output_path
        df = pd.read_excel(fr"{self.output_path}\FinishTimes.xlsx")
        df2 = pd.read_excel(fr"{self.output_path}\TotEnergyConsumption.xlsx")
        data = dict()
        if 'th' in request['output']:
            data["average_TH"] = 1/df["ExitTime"].diff().mean()
        if 'st' in request['output']:
            # Seleziona la quarta colonna (colonna dei cycle time)
            system_time = df["CycleTime"]
            data["average_system_time"] = system_time[system_time >= 0].mean()
        if 'energy' in request['output']:
            # Calcola il consumo energetico totale
            data["total_energy_consumption"] = np.sum(df2.iloc[-1,1:].astype(float))
        if 'Cmax' in request['output'] or 'makespan' in request['output']:
            data["Cmax"] = df['ExitTime'].max()
        return data

class DigitalTwin(DigitalTwin):
    def start(self):
        #freeze
        super().start()

def _clean_win32com():
    import win32com
    from os import rename
    path = win32com.__gen_path__
    path = path.rsplit('\\',1)[0]
    print(path)

if __name__ == '__main__':
    dt = DigitalTwin()
    dt.start()
    dt.stop()


