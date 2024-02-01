import asyncio
import time
from DTPPC.implementation.local.planned_orders import planned_orders_simplified
from DTPPC.implementation.local.running_orders import running_orders
from DTPPC.implementation.controller.controller import SmartController

async def create_files(input_file,output_file_po,output_file_ro,timeout,ctrl:SmartController=None):
    while True:
        print("Creating files UP")
        po = planned_orders_simplified(input_file,output_file=output_file_po)
        running_orders(input_file,output_file=output_file_ro)
        if ctrl:
            ctrl.systemModel['orders'] = po
        await asyncio.sleep(timeout)

def create_files(input_file,output_file_po,output_file_ro,timeout,ctrl:SmartController=None):
    flag = False
    while True:
        try:
            po = planned_orders_simplified(input_file,output_file=output_file_po)
            running_orders(input_file,output_file=output_file_ro)
            if ctrl:
                ctrl.systemModel['orders'] = po
            time.sleep(timeout)
            if not flag:
                flag = True
                print("Creating files UP")
        except:
            time.sleep(0.1)
        