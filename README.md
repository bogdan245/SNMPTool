# SNMPTool
A simple SNMP query tool

Pre-requisites: python3, pysnmplib, pysmi >= 0.3.4, pyasn1 >= 0.4.8, configparser, json. (these versions are what I currently have)

It uses pysnmp to get SNMP data based on different MIB codes.
I used the IF-MIB list to get the Operational State of a layer 3 switch interface.


  Basically it is a function which gets the host and interfaces to look for, 
and returns the status UP or DOWN, pretty simple.

In future updates I will try to make it so it can get more SNMP traps.
