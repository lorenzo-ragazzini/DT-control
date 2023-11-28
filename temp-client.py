import requests
import asyncio
from DTPPC.implementation.cloud.cloud import upload
from DTPPC.implementation.controller.trigger import Trigger
from DTPPC.implementation.flask.front import DTInterface
from DTPPC.implementation.controller.controller import SmartController, ExecuteSchedule, Release, GenerateSchedule, SetWIP, ControlMap, Rule1, Rule2, Rule3, Rule4
from DTPPC.implementation.local.create_files import create_files
from DTPPC.implementation.local.dbConnect import DBConnection
from DTPPC.implementation.local.events import EventCreator
from DTPPC.implementation.local.planned_orders import planned_orders

if __name__ == '__main__':

    filename = 'MESdata.xlsx'
    file_path = ''
    running_orders_file = ''
    cloud_file_path = ''

    dt = DTInterface("127.0.0.1:5000")
    dbc = DBConnection(file_path,filename)
    ec = EventCreator(file_path,filename,output_filename='log.json')
    t = Trigger(file_path,filename)

    ctrl = SmartController()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5), GenerateSchedule(), SetWIP()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]

    t.controller = ctrl

    asyncio.run(dbc.run_async(timeout=5)) # convert MES accdb to xlsx
    asyncio.run(create_files(timeout=5,ctrl=ctrl)) # create input files
    upload(running_orders_file,file_path,cloud_file_path,timeout=5) # upload files to Azure cloud
    asyncio.run(ec.run_async(5)) # read events
    asyncio.run(t.run_async(5)) # trigger events

'''
dt = DTInterface("127.0.0.1:5000")

ctrl = SmartController()
ctrl.dt = dt
ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5), GenerateSchedule(), SetWIP()]
ctrl.linkPolicies()
ctrl.map = ControlMap()
ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
ctrl.systemModel['orders'] = planned_orders()
ctrl.send('start')
'''