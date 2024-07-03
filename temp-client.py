from os import getcwd
import subprocess
import asyncio
from DTPPC.implementation.cloud.cloud import upload as cloud_upload
from DTPPC.implementation.controller.trigger import Trigger
from DTPPC.implementation.flask.front import DTInterface
from DTPPC.implementation.controller.controller import create_controller, SmartController, ExecuteSchedule, ReleaseOne, GenerateSchedule, SetWIP, ControlMap, Rule1, Rule2, Rule3, Rule4
from DTPPC.implementation.local.actuator import Actuator
from DTPPC.implementation.local.create_files import create_files
from DTPPC.implementation.local.dbConnect import DBReader
from DTPPC.implementation.local.events import EventCreator
from DTPPC.implementation.local.planned_orders import planned_orders_simplified

import warnings 
import json
warnings.filterwarnings('ignore') 

async def run_tasks(db_file,planned_orders_file,running_orders_file,running_orders_path,cloud_file_path):
    ''' For compatibility with Windows 7'''
    def get_coroutines():
        coroutines = [
            dbc.run_async(timeout=1),  # convert MES accdb to xlsx
            create_files(input_file=db_file, output_file_po=planned_orders_file, output_file_ro=running_orders_file, timeout=1, ctrl=ctrl),  # create input files & transfers the order to the controller
            # eventCreator.run_async(5),  # read events
            trigger.run_async(1),  # trigger events
            cloud_upload(running_orders_filename,running_orders_path,cloud_file_path,timeout=5) # upload files to Azure cloud
        ]
        return coroutines
    tasks = [asyncio.create_task(coro) for coro in get_coroutines()]
    
    await asyncio.gather(*get_coroutines())

    while True:
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            index = tasks.index(task)
            tasks.remove(task)
            new_task = asyncio.create_task(get_coroutines()[index])
            tasks.append(new_task)

if __name__ == '__main__':
    debug_client:bool = False
    debug_server:bool = False        
    system:str = "WIN7"
    python_version = "3.9"
      
    running_orders_file = getcwd()+'\WorkInProcess.txt'
    planned_orders_file = ''
    cloud_file_path = 'dt-input/'
    running_orders_path, running_orders_filename = running_orders_file.rsplit('\\',1)
    running_orders_path += "\\"
    
    subprocess.Popen(["cmd.exe", "/k", python_version, "DTPPC/implementation/popup/visual/notifier.py"])
    
    if not debug_client:
        db_file = 'MESdata.xlsx'
    else:
        db_file = "C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESdebug.xlsx"
    if not debug_server:
        try:
            # Load configuration from config.json file
            with open('config.json') as f:
                config = json.load(f)
            address = config['tunnel_string']
        except:
            # manually
            address="https://34a3-131-175-147-135.ngrok-free.app" #without final /; if error, wait after starting the server
    else:
        address="http://127.0.0.1:5000"

    dt = DTInterface(address) # interface with the DT
    dbc = DBReader(output_file=db_file) # read the ACCDB defined in DBReader class, write db_file
    eventCreator = EventCreator(db_file,output_file='log.json') # create log.json file listening to events
    trigger = Trigger(db_file) # trigger > self.controller
    ctrl = create_controller() # get preset controller
    act = Actuator() # prints decision variables onto the MES ACCDB
	
    ctrl.dt = dt # connect the controller to the DT
    trigger.controller = ctrl # connect the trigger to the controller
    ctrl.actuator = act # connect the controller to the actuator
    
    if debug_client == True:
        # support debugging
        ctrl.systemModel['orders'] = planned_orders_simplified("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESdebug.xlsx")
        ctrl.init_dv()
    
        # make experiments
        # asyncio.run(ctrl.send("startUnscheduled"))
        ctrl.send_async("startUnscheduled")

    if system == "WIN7":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_tasks(db_file,planned_orders_file,running_orders_file,running_orders_path,cloud_file_path))
    else:
        asyncio.run(dbc.run_async(timeout=5)) # convert MES accdb to xlsx
        asyncio.run(create_files(input_file=db_file,output_file_po=planned_orders_file,output_file_ro=running_orders_file,timeout=5,ctrl=ctrl)) # create input files & transfers the order to the controller
        asyncio.run(cloud_upload(running_orders_filename,running_orders_path,cloud_file_path,timeout=5)) # upload files to Azure cloud
        asyncio.run(eventCreator.run_async(5)) # read events
        asyncio.run(trigger.run_async(5)) # trigger events