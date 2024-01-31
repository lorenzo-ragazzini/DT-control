from os import getcwd
import requests
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

async def run_tasks(db_file,planned_orders_file,running_orders_file,running_orders_path,cloud_file_path):
    ''' For compatibility with Windows 7'''
    def get_coroutines():
        coroutines = [
            dbc.run_async(timeout=5),  # convert MES accdb to xlsx
            create_files(input_file=db_file, output_file_po=planned_orders_file, output_file_ro=running_orders_file, timeout=5, ctrl=ctrl),  # create input files & transfers the order to the controller
            ec.run_async(5),  # read events
            trigger.run_async(5),  # trigger events
            cloud_upload(running_orders_filename,running_orders_path,cloud_file_path,timeout=5) # upload files to Azure cloud
        ]
        return coroutines
    tasks = [asyncio.create_task(coro) for coro in get_coroutines()]
    
    while True:
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            index = tasks.index(task)
            tasks.remove(task)
            new_task = asyncio.create_task(get_coroutines()[index])
            tasks.append(new_task)

		
if __name__ == '__main__':
    debug:bool = True
    mode:str = "WIN7"
    
    db_file = 'MESdata.xlsx'
    if debug == True:
        db_file = "C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx"
    
    running_orders_file = getcwd()+'\WorkInProcess.txt'
    planned_orders_file = ''
    cloud_file_path = 'dt-input/'
    address="127.0.0.1:5000" 

    dt = DTInterface(address) # interface with the DT
    dbc = DBReader(output_file=db_file) # read the ACCDB defined in DBReader class, write db_file
    ec = EventCreator(db_file,output_file='log.json') # create log.json file listening to events
    trigger = Trigger(db_file) # trigger > self.controller
   
    ctrl = create_controller() # get preset controller
    act = Actuator() # prints decision variables onto the MES ACCDB
	
    ctrl.dt = dt
    trigger.controller = ctrl
    ctrl.actuator = act
    
    if debug == True:
        ctrl.systemModel['orders'] = planned_orders_simplified("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx")
        ctrl.init_dv()
        asyncio.run(ctrl.SetWIP.solve())
        # asyncio.run(ctrl.send("start"))

    running_orders_path, running_orders_filename = running_orders_file.rsplit('\\',1)
    running_orders_path += "\\"

    if mode == "WIN7":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_tasks(db_file,planned_orders_file,running_orders_file,running_orders_path,cloud_file_path))
    else:
        asyncio.run(dbc.run_async(timeout=5)) # convert MES accdb to xlsx
        asyncio.run(create_files(input_file=db_file,output_file_po=planned_orders_file,output_file_ro=running_orders_file,timeout=5,ctrl=ctrl)) # create input files & transfers the order to the controller
        asyncio.run(cloud_upload(running_orders_filename,running_orders_path,cloud_file_path,timeout=5)) # upload files to Azure cloud
        asyncio.run(ec.run_async(5)) # read events
        asyncio.run(trigger.run_async(5)) # trigger events