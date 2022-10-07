from pysnmp.hlapi import *
import time, sys, os, configparser, json


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



intDict = {}
intList = [] #interfaces dict
def SNMPinspect( specifyHost, specifyInterface):

    for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                CommunityData('public', mpModel=0),
                                UdpTransportTarget((f'{specifyHost}', 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', f'{specifyInterface}')),
                                 ):

        resultDict = {}
        if errorIndication or errorStatus:
            with open("log.txt", "w") as log_file:
                log_file.write(errorIndication or errorStatus)
            break
        else:
            for bind in varBinds:
                #print(bind.prettyPrint())
                intList.append(bind[1].prettyPrint())



#parse the interfaces list and apply function defined above
for j in range (len(host_list)):
    for i in range(len(ifList)):
        SNMPinspect(host_list[j], ifList[i])
    intDict[host_list[j]] = intList
#print(OPTION, type(OPTION))

with open("returned_json\\output.json", 'w') as output:
    output.write(json.dumps(intDict))



#print(intList)

