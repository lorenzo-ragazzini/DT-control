import json
import pandas as pd
from azure.storage.queue import QueueServiceClient


def read_excel_file(file_path):
    xls = pd.ExcelFile(file_path)
    excel_data = {}
    for sheet_name in xls.sheet_names:
        sheet_data = xls.parse(sheet_name)
        excel_data[sheet_name] = sheet_data.to_json(orient='records')
    return excel_data

# print(read_excel_file("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx"))

class Upload:
    def __init__(self,queue_name=None):
        self.path_to_file = None
        self.filename = None
        self.queue_name = queue_name
    def run(self):
        connection_string = 'DefaultEndpointsProtocol=https;AccountName=cloudformesdata;AccountKey=V3a7emh71+MSTdHykDKaZS9NPzwlp/orebGlYCNGNet5PgRgl7o94lafftuIO1JaOc+sNjFisdCt+AStR14uag==;EndpointSuffix=core.windows.net'
        queue_service_client = QueueServiceClient.from_connection_string(connection_string)
        queue_client = queue_service_client.get_queue_client(self.queue_name)

        # data = pd.read_excel(self.path_to_file+self.filename).to_json()
        data = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 22]})
        data = read_excel_file("C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB/MESb.xlsx")
        for key in data.keys():
            data[key]=data[key]

        # Enqueue the JSON string as a message
        queue_client.send_message(data)

u=Upload(queue_name="dt-input")
u.run()

class Download:
    pass

