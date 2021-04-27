from flask import Flask, render_template, jsonify
from influxdb import InfluxDBClient

def makeConnection():
    client = InfluxDBClient(host='10.106.79.198',port=8086)
    client.switch_database('telegraf')
    pim_data = client.query('SELECT "source", "neighbor_address_xr/ipv4_address" AS IP, "is_this_neighbor_us", "interface_name" FROM "Cisco-IOS-XR-ipv4-pim-oper:pim/active/default-context/neighbors/neighbor" WHERE time > now() - 30s GROUP BY "source"')
    igmp_data = client.query('SELECT "source", "group_address", "interface_name", "last_reporter/ipv4_address" FROM "Cisco-IOS-XR-ipv4-igmp-oper:igmp/active/default-context/groups/group" WHERE group_address =~/^232.[0-9]+.[0-9]+.[0-9]+/ AND time > now() - 30s GROUP BY "source"')
    ssm_flow_data = client.query('SELECT "source", "group_address", "source_address", "protocol", "rpf_interface_name", "rpf_neighbor/ipv4_address", "outgoing_interface/interface_name", "last_hop", "alive", "really_alive" FROM "Cisco-IOS-XR-ipv4-pim-oper:pim/active/default-context/topologies/topology" WHERE group_address =~/^232.[0-9]+.[0-9]+.[0-9]+/ AND time > now() - 40s GROUP BY "group_address"')
    sparse_data = client.query('SELECT "source", "group_address", "source_address", "rp_address/ipv4_address", "protocol", "rpt", "rpf_interface_name", "rpf_neighbor/ipv4_address", "outgoing_interface/interface_name", "alive", "last_hop" FROM "Cisco-IOS-XR-ipv4-pim-oper:pim/active/default-context/topologies/topology" WHERE group_address =~/^225.[0-9]+.[0-9]+.[0-9]+/ AND time > now() - 30s GROUP BY "group_address"')
    # print(sparse_data)
    return pim_data,igmp_data,ssm_flow_data,sparse_data