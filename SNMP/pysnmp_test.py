from pysnmp.hlapi import *
import time, sys, os, configparser


# Reading configuration files

config = configparser.ConfigParser()
config.read('CONFIG_FILES\\hosts.ini') #hosts config file
hosts = config.sections()

hostOptions = config.options('HOSTS')
hostItems = config.items('HOSTS')


# Make hosts list to parse it further
host_list = []
for host in range(len(hostItems)):
    host_list.append(hostItems[host][1])


#Get mib + option + interface
config.read("CONFIG_FILES\\mib_codes.ini")
mibs = config.sections()

mibItems = config.items('MIB')
MIB = mibItems[0][1]
OPTION = mibItems[1][1]

interfaces = config.items('INTERFACES')

#next make interfaces codes list
ifList = []
for interface in range(len(interfaces)):
    ifList.append(interfaces[interface][1])

def SNMPinspect(specifymib, specifyoption, specifyInterface):
    for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                CommunityData('public', mpModel=0),
                                UdpTransportTarget(('192.168.10.1', 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity(str(specifymib), str(specifyoption), str(specifyInterface))),
                                 ):
        if errorIndication or errorStatus:
            print(errorIndication or errorStatus)
            break
        else:

            for i in range(0,len(varBinds)):
                portUp = "Is UP"
                portDown = "Is Down"
                if str(varBinds[i][1]) == 'up':
                    print("Port " + str(i+1) + " " + portUp)
                elif str(varBinds[i][1]) == 'down':
                    print("Port " + str(i+1) + " " + portDown)
                else:
                    print("Stare port necunoscuta")








