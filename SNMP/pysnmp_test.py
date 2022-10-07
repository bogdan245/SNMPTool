from pysnmp.hlapi import *
import configparser
import json


# Reading configuration files

config = configparser.ConfigParser()
config.read('CONFIG_FILES\\hosts.ini')  # hosts config file
hosts = config.sections()

hostOptions = config.options('HOSTS')
hostItems = config.items('HOSTS')


# Make hosts list to parse it further
host_list = []
for host in range(len(hostItems)):
    host_list.append(hostItems[host][1])


# Get mib + option + interface
config.read("CONFIG_FILES\\mib_codes.ini")
mibs = config.sections()

mibItems = config.items('MIB')
MIB = mibItems[0][1]
OPTION = mibItems[1][1]

interfaces = config.items('INTERFACES')

# next make interfaces codes list
ifList = []
for interface in range(len(interfaces)):
    ifList.append(interfaces[interface][1])  # Interfaces list

# This part is to define the function that gets two variables, a HOST and an INTERFACE
intDict = {}  # dict to construct interfaces status per host
intList = []  # interfaces list
hostDict = {}  # dictionary with status per interface inside host


def snmp_inspect(specify_host, specify_interface):

    for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in getCmd(SnmpEngine(),
                                CommunityData('public', mpModel=0),
                                UdpTransportTarget((f'{specify_host}', 161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', f'{specify_interface}')),
                                ):

        if errorIndication or errorStatus:
            with open("log.txt", "w") as log_file:
                log_file.write(errorIndication or errorStatus)
            break
        else:
            for bind in varBinds:
                intList.append(bind[1].prettyPrint())

# parse the hosts list, then the interfaces list per host,
# then an additional for loop to get interfaces names and
# make the final dictionary with results


for j in range(len(host_list)):
    for i in range(len(ifList)):
        snmp_inspect(host_list[j], ifList[i])
        for k in range(len(intList)):
            hostDict['interface ' + ifList[i][2:]] = intList[k]
    intDict[host_list[j]] = hostDict


# dump in json file
with open("returned_json\\output.json", 'w') as output:
    output.write(json.dumps(intDict))

# dump in javascript file to process it later if needed
with open("returned_json\\output.js", 'w') as json_formatted:
    jsonobj = json.dumps(intDict)
    json_formatted.write("var jsonstr = '{}'".format(jsonobj))
    json_formatted.close()