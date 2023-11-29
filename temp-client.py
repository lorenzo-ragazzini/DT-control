import os
import requests
import asyncio
from DTPPC.implementation.cloud.cloud import upload
from DTPPC.implementation.controller.trigger import Trigger
from DTPPC.implementation.flask.front import DTInterface
from DTPPC.implementation.controller.controller import create_controller, SmartController, ExecuteSchedule, ReleaseOne, GenerateSchedule, SetWIP, ControlMap, Rule1, Rule2, Rule3, Rule4
from DTPPC.implementation.local.create_files import create_files
from DTPPC.implementation.local.dbConnect import DBConnection
from DTPPC.implementation.local.events import EventCreator
from DTPPC.implementation.local.planned_orders import planned_orders_simplified

if __name__ == '__main__':

    db_file = 'MESdata.xlsx'
    db_file = "C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx" #debug
    running_orders_file = os.getcwd()+'\WorkInProcess.xlsx'
    planned_orders_file = ''
    cloud_file_path = 'dt-input/'

    dt = DTInterface("127.0.0.1:5000")
    dbc = DBConnection(output_file=db_file)
    ec = EventCreator(db_file,output_file='log.json')
    t = Trigger(db_file)
    '''
    ctrl = SmartController()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), ReleaseOne(WIPlimit=5), GenerateSchedule(), SetWIP()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
    '''
    ctrl = create_controller()
    ctrl.dt = dt
    t.controller = ctrl
    ctrl.systemModel['orders'] = planned_orders_simplified("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx")
    #debug
    asyncio.run(ctrl.send_async('startUnscheduled'))
    asyncio.run(ctrl.send_async('completion'))

    # asyncio.run(dbc.run_async(timeout=5)) # convert MES accdb to xlsx
    # asyncio.run(create_files(input_file=db_file,output_file_po=planned_orders_file,output_file_ro=running_orders_file,timeout=5,ctrl=ctrl)) # create input files
    # running_orders_path, running_orders_filename = running_orders_file.rsplit('\\',1)
    # running_orders_path += "\\"
    # asyncio.run(upload(running_orders_filename,running_orders_path,cloud_file_path,timeout=5)) # upload files to Azure cloud
    asyncio.run(ec.run_async(5)) # read events
    # asyncio.run(t.run_async(5)) # trigger events
    print('finished')

'''
dt = DTInterface("127.0.0.1:5000")

ctrl = SmartController()
ctrl.dt = dt
ctrl.policies = [ExecuteSchedule(), ReleaseOne(WIPlimit=5), GenerateSchedule(), SetWIP()]
ctrl.linkPolicies()
ctrl.map = ControlMap()
ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
ctrl.systemModel['orders'] = planned_orders()
ctrl.send('start')
'''