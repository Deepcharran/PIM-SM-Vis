def SSM_Flows(ssm_flow_data,igmp_result,pim_topology,total_routers,total_source_target):
    ssm_flow_result=[]
    ssm_flow_ans={}
    # print(pim_topology)
    for i in ssm_flow_data:
        for j in i:
            del j['time']
    for i in ssm_flow_data:
        for j in i:
            for k in igmp_result:
                if j['source']==k['IGMP Neighbor'] and j['outgoing_interface/interface_name']==k['IGMP Neighbor Interface']:
                    ssm_flow_ans['source']=k['IGMP Source']
                    ssm_flow_ans['target']=k['IGMP Neighbor']
                    ssm_flow_ans['group']=j['group_address']
                    ssm_flow_result.append(ssm_flow_ans)
                    ssm_flow_ans={}
    for i in ssm_flow_data:
        for j in i:
            for k in pim_topology:
                if j['source']==k['Neighbor Name'] and j['rpf_interface_name']==k['Neighbor Interface']:
                    ssm_flow_ans['source']=k['Source Name']
                    ssm_flow_ans['target']=k['Neighbor Name']
                    ssm_flow_ans['group']=j['group_address']
                    ssm_flow_result.append(ssm_flow_ans)
                    ssm_flow_ans={}

    for i in ssm_flow_data:
        for j in i:
            if j['source_address']==j['rpf_neighbor/ipv4_address']:
                ssm_flow_ans['source']= j['source']
                ssm_flow_ans['target']= 'Multicast Source'
                ssm_flow_ans['group']=j['group_address']
                ssm_flow_result.append(ssm_flow_ans)
                ssm_flow_ans={}


    ssm_flow_details=[]
    for i in ssm_flow_result:
        if i not in ssm_flow_details:
            ssm_flow_details.append(i)

    for i in ssm_flow_details:
        if {'id':i['target']} not in total_routers:
            total_routers.append({'id':i['target']})

    # print(total_source_target)
    temp={}
    for i in ssm_flow_details:
        temp["source"]=i["source"]
        temp["target"]=i["target"]
        if temp not in total_source_target:
            total_source_target.append(temp)
    
    # print(ssm_flow_details)
    nonegroup={}
    for i in total_source_target:
        if not i['target'].startswith('Multicast'):
            nonegroup['source']=i['source']
            nonegroup['target']=i['target']
            nonegroup['group']='None'
            ssm_flow_details.append(nonegroup)
            nonegroup={}

    ssm_groups=[]
    #ssm_groups.append('None')
    for i in ssm_flow_details:
        if i['group'] not in ssm_groups:
            ssm_groups.append(i['group'])
    
    return ssm_groups,ssm_flow_details