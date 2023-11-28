import asyncio
from DTPPC.implementation.local.planned_orders import planned_orders_simplified
from DTPPC.implementation.local.running_orders import running_orders
from DTPPC.implementation.controller.controller import SmartController

async def create_files(timeout,ctrl:SmartController=None):
    po = planned_orders_simplified()
    running_orders()
    if ctrl:
        ctrl.systemModel['orders'] = po
    asyncio.sleep(timeout)