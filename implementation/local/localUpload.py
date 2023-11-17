from dtcontrol.implementation.communication.communication import ShareFile, ShareFileOnly
from .syncOrders import planned_orders
from .inputProcessing import running_orders
import asyncio

async def u1(timeout):
    running_orders()
    u1=ShareFileOnly('','WorkInProcess.xlsx','dt-input/')
    u1.upload()
    await asyncio.sleep(timeout=timeout)
async def u2(timeout):
    planned_orders()
    u2=ShareFileOnly('Order_Table.xlsx','','ctrl-input/planned-orders')
    u2.upload()
    await asyncio.sleep(timeout=timeout)


if __name__ == '__main__':
    main()