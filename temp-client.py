import requests
from DTPPC.implementation.flask.front import DTInterface
dt = DTInterface("127.0.0.1:5000")
a=dt.new()
dt.clear()