from azure.storage.queue import QueueServiceClient

class Messenger:
    def __init__(self,delete_received_messages=True):
        self.connection_string = 'DefaultEndpointsProtocol=https;AccountName=cloudformesdata;AccountKey=V3a7emh71+MSTdHykDKaZS9NPzwlp/orebGlYCNGNet5PgRgl7o94lafftuIO1JaOc+sNjFisdCt+AStR14uag==;EndpointSuffix=core.windows.net'
        self.queue_service_client = QueueServiceClient.from_connection_string(self.connection_string)      
    def send(self,queue_name,msg):
        queue_client = self.queue_service_client.get_queue_client(queue_name)
        queue_client.send_message(msg)
    def receive(self,queue_name,delete=True):
        queue_client = self.queue_service_client.get_queue_client(queue_name)
        messages = [m for m in queue_client.receive_messages()]
        for message in messages:
            queue_client.delete_message(message)
        return messages

class MessengerOnly(Messenger):
    def __init__(self,queue_name):
        self.queue_name = queue_name
        super().__init__()
    def send(self,msg):
        super().send(msg,self.queue_name)
    def receive(self):
        return super().receive(self.queue_name)
