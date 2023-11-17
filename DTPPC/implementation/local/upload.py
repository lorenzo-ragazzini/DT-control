from DTPPC.implementation.communication.sharefile import ShareFile, ShareFileOnly
from .planned_orders import planned_orders
from .running_orders import running_orders
from .events import EventCreatorMsg
from .dbConnect import Connection
import asyncio

async def upload_files(timeout):
    if 'c' not in locals().keys():
        c=Connection(tbls=["tblStepDef","tblStep","tblOrderPos"],path_to_file='MESb.xlsx')
        c.connect()
    c.save(c.process())
    running_orders()
    u1=ShareFileOnly('','WorkInProcess.xlsx','dt-input/')
    u1.upload()
    planned_orders()
    u2=ShareFileOnly('Order_Table.xlsx','','ctrl-input/planned-orders')
    u2.upload()
    await asyncio.sleep(timeout=timeout)

def upload():
    timeout_files = 5
    timeout_events = 1
    asyncio.run(upload_files(timeout_files), debug=True)
    e = EventCreatorMsg('events')
    asyncio.run(e.async_run(timeout_events), debug=True)

if __name__ == '__main__':
    upload()