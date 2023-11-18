from DTPPC.implementation.communication.message import MessengerOnly
import os

local_path = ''
filename = 'dv.json'

class DVSend:
    def __init__(self,queue_name,timeout=1):
        self.msg = MessengerOnly(queue_name)
        self.log = list()
        self.timeout = timeout
        self.ctrl = None
    def listen(self):
        events = self.msg.receive()
        for event in events:
            if event not in self.log:
                self.log.append(event)
                self.ctrl.send(event.content)
    async def async_listen(self):
        while True:
            events = self.msg.receive()
            for event in events:
                if event not in self.log:
                    print(event)
                    self.log.append(event)
                    asyncio.run(self.ctrl.send(event.content))
            await asyncio.sleep(self.timeout)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.event_type == 'modified':
            print(f"File '{event.src_path}' has been modified.")

def monitor_file_changes(file_path):
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=file_path, recursive=False)
    observer.start()

    try:
        while True:
            # Keep the observer running
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# Replace 'file_to_monitor.txt' with the path of the file you want to monitor
file_path = 'file_to_monitor.txt'
monitor_file_changes(file_path)

