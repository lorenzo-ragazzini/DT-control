from dtInput import ShareFileOnly, MessengerOnly
import asyncio

async def upload(s:ShareFileOnly,timeout):
    while True:
        s.upload()
        await asyncio.sleep(timeout)

async def donwload(s:ShareFileOnly,timeout):
    while True:
        s.download()
        await asyncio.sleep(timeout)

async def msgsend():
    pass

if __name__ == '__main__':
    u = ShareFileOnly('WorkInProcess.xlsx','','dt-input')

def uploader1V1():
    s1 = ShareFileOnly('WorkInProcess.xlsx','','dt-input')
    asyncio.run(upload(u),5)
    s2 = ShareFileOnly('Orders_Table.xlsx','','ctrl-input/planned-orders')
    asyncio.run(upload(u),5)
    m = MessengerOnly('events')

def downloader1V1():
    pass

def uploader2V1():
    m = MessengerOnly('dv')

def downloader2V1():
    pass