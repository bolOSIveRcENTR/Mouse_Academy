'''
Copyright (C) 2018 Meister Lab at Caltech 
-----------------------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import os, sys
import argparse
import traceback
from serial.tools.list_ports_linux import comports

def getDevices():
    iterator = sorted(comports())
    devices = {}
    for port in iterator:
        l = port[1].split(' (')
        portName = port[0]
        device = l[0].strip(')')
        devices.update({device:portName})
        
    print('Devices:')
    for device in devices:
        portname = devices[device]
        print('{}: {}'.format(device, portname))
    return devices

#Toggle DTR to reset serial port
def resetSer(ser):
    ser.setDTR(False)
    time.sleep(0.05)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.setDTR(True)

def findBpodUSBPort():
    foundBpodPort = False
    devices = getDevices()
    for device in devices:
        portname = devices[device]
        if 'Arduino Due' in portname:
            if not 'Prog' in portname:
                bpodPort = portname
                foundBpodPort = True
    if foundBpodPort:
        return bpodPort
    else:
        raise DeviceError('Arduino Due Native USB Port not found.')
        

def findBpodProgPort():
    foundBpodPort = False
    devices = getDevices()
    for device in devices:
        portname = devices[device]
        if 'Arduino Due' in portname:
            if 'Prog' in portname:
                bpodPort = portname
                foundBpodPort = True
    if foundBpodPort:
        return bpodPort
    else:
        raise DeviceError('Arduino Due Programming Port not found.')
    
#determine portname for arduino mega because it doesn't
#have a device name for some reason
def findMegaPort():
    devices = getDevices()
    megaFound = False
    print('Looking for Arduino Mega...')
    for key in devices.keys():
        if 'tty' in key:
            print('Trying port %s...' % devices[key])
            trySer = serial.Serial(devices[key], 9600, timeout=1)
            resetSer(trySer)
            r = trySer.readline()
            rline = r.decode().strip().lower()
            print("Message from serial device: %s" % rline)
            if 'mega' in rline:
                print('Arduino Mega 2560 found on port %s' % devices[key])
                trySer.readline()
                trySer.reset_output_buffer()
                trySer.reset_input_buffer()
                megaFound = True
                megaName = key
                megaSer = trySer
                break
            else:
                trySer.close()
    if not megaFound:
        raise DeviceError('Arduino Mega 2560 not found.')
    
    return megaSer

class DeviceError(Exception):
    pass