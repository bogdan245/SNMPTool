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
    ifList.append(interfaces[interface][1]) #Interfaces list

def SNMPinspect(specifymib, specifyoption, specifyInterface):
    for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                CommunityData('public', mpModel=0),
                                UdpTransportTarget(('192.168.10.1', 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity(f'{specifymib}', f'{specifyoption}', f'{specifyInterface}')),
                                 ):

        if errorIndication or errorStatus:
            with open("log.txt") as log_file:
                log_file.write(errorIndication or errorStatus)
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

#parse the interfaces list and apply function defined above
for i in range(len(ifList)):
    SNMPinspect(MIB, OPTION, ifList[i])

#print(OPTION, type(OPTION))




