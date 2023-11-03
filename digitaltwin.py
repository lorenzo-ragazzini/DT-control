import os
import re
import time
import json
import numpy as np
import pandas as pd
from plantsim.plantsim import Plantsim
from plantsim.table import Table


def plantsim_trigger():
    with open('config.json') as f:
        paths = json.load(f)
        model_path = paths['model_path']
        output_path = paths['output_path']
    plantsim = Plantsim(version = '16.0', license_type='Student')
    plantsim.load_model(model_path)
    plantsim.set_path_context('.Models.Model')
    plantsim.set_event_controller()
    plantsim.reset_simulation()
    plantsim.start_simulation()

    filename = "FinishTimes.xlsx"
    output_path = os.path.join(output_path, filename)
    
    while not os.path.exists(output_path):
        pass

    print(f"Il file nella cartella {output_path} è stato generato.")
    plantsim.quit()


class DigitalTwin():
    def __init__(self) -> None:
        with open('config.json') as f:
            paths = json.load(f)
            self.model_path = paths['model_path']
            self.output_path = paths['output_path']
            self.input_path = paths['input_path']
            self.filename = "FinishTimes.xlsx"        
    def start(self):
        self.plantsim = Plantsim(version = '16.0', license_type='Student')
        self.plantsim.load_model(self.model_path)
        self.plantsim.set_path_context('.Models.Model')
        self.plantsim.set_event_controller()
    def plantsim_run(self):
        self.plantsim.reset_simulation()
        self.plantsim.start_simulation()       
        while not os.path.exists(os.path.join(self.output_path, self.filename)):
            time.sleep(0.1)
        return
    def synchronize(self,taskResourceInformation:dict):
        #tbd
        df_orderpos = pd.read_excel(fr"{self.input_path}\MESb.xlsx", sheet_name="tblOrderPos")
        df_orderpos=df_orderpos[df_orderpos.Start.isna()]
        #tbd
        df = pd.DataFrame()
        df['Number']=1
        df['WPNo'] = df_orderpos['WPNo']
        df['Order']=df_orderpos['ONo'].astype(str) + '-' + df_orderpos['OPos'].astype(str)
        df.to_excel(fr"{self.input_path}\OrdersTable.xlsx", index=False)
    def update(self,controlUpdate:dict):
        controlUpdate['executeSchedule']
        controlUpdate['admission']
    def simulate(self,request,write=False):
        configuration=pd.DataFrame()
        configuration['simLength'] = request['simLength']
        configuration.to_excel(fr"{self.input_path}\Configuration.xlsx", index=False)
        results = dict()
        for ii in range(request['nrOfSimul']):
            self.plantsim_run()
            results[ii] = self.output_analysis()
        if len(results) == 1:
            results = results[1]
        if not write:
            return results
        else:
            with open('results.json', 'w') as f:
                json.dump(results, f)
            return
    def interface(self,request,taskResourceInformation:dict=None,controlUpdate=None,write=False)->None:
        self.synchronize(taskResourceInformation)
        self.update(controlUpdate)
        return self.simulate(request)
    def output_analysis(self,request)->dict:
        self.output_path
        df = pd.read_excel(fr"{self.output_path}\FinishTimes.xlsx")
        df2 = pd.read_excel(fr"{self.output_path}\TotEnergyConsumption.xlsx")
        data = dict()
        if 'th' in request['output']:
            # Seleziona la colonna dei tempi di uscita
            tout = df.iloc[:, 1]
            # Calcola le differenze tra i tempi di uscita
            dt = tout.diff()
            # Calcola la media dei tempi di attraversamento del sistema
            average_throughput = 1/dt.mean()
            data["average_TH"] = average_throughput
        if 'ct' in request['output']:
            # Seleziona la quarta colonna (colonna dei cycle time)
            cycle_time = df.iloc[:, 3]
            # Filtra i valori negativi
            cycle_time = cycle_time[cycle_time >= 0]
            # Calcola la media dei valori del cycle time
            average_cycle_time = cycle_time.mean()
            data["average_CT"] = average_cycle_time
        if 'energy' in request['output']:
            # Calcola il consumo energetico totale
            total_energy_consumption = np.sum(df2.iloc[-1,1:].astype(float))
            data["total_energy_consumption"] = total_energy_consumption
        return data


