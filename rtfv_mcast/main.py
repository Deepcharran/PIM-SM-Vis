from flask import Flask, render_template, jsonify
from influxdb import InfluxDBClient
import DatabaseConnection
import Topology
import PimSSM
import SparseMode

application = Flask(__name__)

def influxdbfun():
    pim_data,igmp_data,ssm_flow_data,sparse_data = DatabaseConnection.makeConnection()
    topology,total_routers,total_source_target,igmp_result,pim_topology = Topology.makeTopology(pim_data,igmp_data)
    ssm_groups,ssm_flow_details = PimSSM.SSM_Flows(ssm_flow_data,igmp_result,pim_topology,total_routers,total_source_target)
    sparse_traffic_result,sparse_no_traffic_result,sm_groups,rp_router = SparseMode.SparseFlows(sparse_data,igmp_result,pim_topology,total_source_target)
    
    # print(sm_groups)
    # print(sparse_no_traffic_result)
    # print(sparse_traffic_result)
    
    return (total_routers, total_source_target, topology, ssm_flow_details,ssm_groups,sparse_no_traffic_result,sparse_traffic_result, sm_groups,rp_router)
    

@application.route('/update_decimal', methods=['POST'])
def updatedecimal():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups, rp_router = influxdbfun()
    return {"w": routernames, "x": source_target, "y": result, "z": flow_details,"v": ssm_groups,"u1":sparse_no_traffic_result,"v1":sparse_traffic_result,"w1":sm_groups,"x1":rp_router}


@application.route('/')
def homepage():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups,rp_router= influxdbfun()
    return render_template('home.html', w=routernames, x=source_target, y=result, z=flow_details, v=ssm_groups)

@application.route('/pimssm.html')
def pimssm_vis():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups, rp_router= influxdbfun()
    return render_template('pimssm.html', w=routernames, x=source_target, y=result, z=flow_details, v=ssm_groups)

@application.route('/pimsm.html')
def pimsm_vis():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups, rp_router= influxdbfun()
    return render_template('pimsm.html', u1=sparse_no_traffic_result,v1=sparse_traffic_result,w1=sm_groups, w=routernames, y=result, x1=rp_router)

@application.route('/topology.html')
def topology_vis():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups, rp_router= influxdbfun()
    return render_template('topology.html', w=routernames, x=source_target, y=result, z=flow_details, v=ssm_groups)

@application.route('/admin.html')
def admin_vis():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups, rp_router= influxdbfun()
    return render_template('admin.html', w=routernames, x=source_target, y=result, z=flow_details, v=ssm_groups)

@application.route('/about.html')
def about_vis():
    routernames, source_target, result, flow_details, ssm_groups, sparse_no_traffic_result,sparse_traffic_result, sm_groups, rp_router= influxdbfun()
    return render_template('about.html', w=routernames, x=source_target, y=result, z=flow_details, v=ssm_groups)

if __name__ == '__main__':
    application.run(host='0.0.0.0',port=5000,debug=False,)
