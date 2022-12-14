#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_snmp.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : GPL-3.0
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------
# Import Python Modules.
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp import hlapi
import re

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
    return pairs

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids))
    return fetch(handler, 1)[0]

def set(target, value_pairs, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.setCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_value_pairs(value_pairs))
    return fetch(handler, 1)[0]

def get_bulk(target, oids, credentials, count, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        start_from, count,
        *construct_object_types(oids))
    return fetch(handler, count)

def get_bulk_auto(target, oids, credentials, count_oid, start_from=0, port=161,
                  engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    count = get(target, [count_oid], credentials,
                port, engine, context)[count_oid]
    return get_bulk(target, oids, credentials, count, start_from, port, engine, context)

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(
                handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError(
                    'Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def snmpmac(dev_ip, snmpcs, snmp_oid):
    """
    MAC Address Collector and formatter
    """
    # SNMP oid for MAC Address on Xerox Remote Devices.
    snmp_oid = snmp_oid
    # Define a PySNMP CommunityData object named auth, by providing the SNMP community string
    auth = cmdgen.CommunityData(snmpcs)
    # Define the CommandGenerator, which will be used to send SNMP queries
    cmdGen = cmdgen.CommandGenerator()
    # Query a network device using the getCmd() function, providing the auth object, a UDP transport
    # our OID for MAC ADDR, and don't lookup the OID in PySNMP's MIB's
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        auth,
        cmdgen.UdpTransportTarget((dev_ip, 161)),
        cmdgen.MibVariable(snmp_oid),
        lookupMib=False,)
    # Check if there was an error querying the device
    if errorIndication:
        return None
        return errorIndication
    for oid, val in varBinds:
        #print(oid.prettyPrint(), val.prettyPrint())
        macval = val.prettyPrint()
        macaddr = ':'.join(re.findall('..', macval[2:]))
        return (macaddr.upper())