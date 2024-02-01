# -*- coding: utf-8 -*-
from time import sleep
from DTPPC.operationalController import ControlModule
from DTPPC.controller.misc import SimulationRequest
from DTPPC.controller.misc import genControlUpdate
import pandas as pd
import numpy as np

class SetWIP(ControlModule):
    inputParameters = ['orders']
    def __init__(self,timeout=600) -> None:
        self.timeout = timeout
    def solve(self,**kwargs):
        sleep(10) #initial timeout
        while True:
            input = self._controller.search(self.inputParameters)
            taskResourceInformation = input['orders'].to_dict()
            r = list()
            DTname = self._controller.dt.new()
            # taskResourceInformation = self._controller.systemModel['orders'].to_dict()
            ctrlUpdate = genControlUpdate(self._controller)
            for WIPlevel in range(1,10):
                ctrlUpdate['ReleaseOne']['CONWIP_value'] = WIPlevel
                req = SimulationRequest()
                req['output'] = ['th','st']
                res = self._controller.dt.interface(DTname,taskResourceInformation,ctrlUpdate,req)
                r.append([WIPlevel,res['average_TH'],res["average_system_time"]])
            r = pd.DataFrame(r,columns=["WIP","TH","LT"]).set_index(['WIP'])
            plot(r)
            WIPlevel = np.random.randint(4,7)
            print("Target WIP is set to %d" %WIPlevel)
            self._controller.dt.clear(DTname)
            sleep(self.timeout)

def plot(df):
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df.index, df['TH'], marker='o', label='TH', color='b')
    ax1.set_xlabel('WIP')
    ax1.set_ylabel('TH', color='b')
    ax1.tick_params('y', colors='b')
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['LT'], marker='s', label='LT', color='r')
    ax2.set_ylabel('LT', color='r')
    ax2.tick_params('y', colors='r')
    fig.legend(loc='upper left', bbox_to_anchor=(0.15, 0.85))
    plt.title('TH and LT as functions of WIP')
    plt.show(block=False)  # Display the plot without blocking
    plt.pause(3)  # Pause for 5 seconds
    plt.close()  # Close the plot window after 5 seconds

    