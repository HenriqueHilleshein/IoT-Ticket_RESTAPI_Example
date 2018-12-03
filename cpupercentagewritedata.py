import time
import json
import sys
import datetime
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import vts
from iotticket.models import datanodesvalue
from iotticket.client import Client
import psutil

def kill_process():
    file = open("pidfile", "r")
    pid = file.read()
    p = psutil.Process(int(pid))
    p.kill()

data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
deviceId = ""
if 'deviceId' in data:
    deviceId = data["deviceId"]
baseurl = data["baseurl"]
c = Client(baseurl, username, password)
if(c!="404 URL NOT FOUND!!!"):
    if deviceId == "": # It's not registered yet, it need to be regitered.
        d = device()
        d.set_name("Register Test")
        d.set_manufacturer("Dell")
        d.set_type("PC")
        d.set_description("More register")
        registeredDevice = c.registerdevice(d)
        data["deviceId"] = registeredDevice.deviceId
        deviceId = registeredDevice.deviceId
        json.dump(data,open(sys.argv[1], "w"))
    # Creating the data tags and set the default values
    nv = datanodesvalue()
    nv.set_name("Processor")
    nv.set_path("fedora/percentVal")
    nv.set_dataType("double")
    killOrdernv = datanodesvalue()
    killOrdernv.set_name("orderToKill")
    killOrdernv.set_path("fedora/kill")
    killOrdernv.set_dataType("boolean")
    killOrdernv.set_timestamp(c.dttots(datetime.datetime.now()))
    killOrdernv.set_value(False)
    c.writedata(deviceId, killOrdernv)
    # It's used configure which variiables will be read from the server
    cr = criteria()
    cr.set_criterialist("orderToKill") # Variable that says that the process need to be killed
    while 1:
        # Get cpu percent
        data = c.readdata(deviceId, cr)
        shouldKill = data.get_attributes()[0].get_values()[0].get_value()
        if shouldKill == "true":
            kill_process()
            killOrdernv.set_timestamp(c.dttots(datetime.datetime.now()))
            killOrdernv.set_value(False)
            c.writedata(deviceId, killOrdernv)
        cpuPercent = psutil.cpu_percent()
        #set the value of the node with the cpu usage value
        nv.set_value(cpuPercent)
        #set the timestamp as now
        nv.set_timestamp(c.dttots(datetime.datetime.now()))
        #call writedata function
        c.writedata(deviceId, nv)
        #the program will run every 2 seconds
        time.sleep(2)
else:
    print(c)
