import sys
sys.path.append('C:\mats\git_mats\DeviceSocketInterface/code')
from device_interface import DeviceSocketInterface as DSI
sys.path.remove('C:\mats\git_mats\DeviceSocketInterface/code')

ati = DSI(host='192.168.3.15',port=49152)
