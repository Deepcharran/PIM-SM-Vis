def SparseFlows(sparse_data,igmp_result,pim_topology,total_source_target):
    # print(igmp_result)
    # print(pim_topology)
    # print(sparse_data)
    sparse_traffic_data=[]
    std=[]
    sntd=[]
    sparse_no_traffic_data=[]
    for i in sparse_data:
        for j in i:
            if j['source_address']=='0.0.0.0':
                sntd.append(j)
            else:
                std.append(j)

    for i in sntd:
        del i['time']
    for i in std:
        del i['time']

    # print(sntd)
    for i in sntd:
        if i not in sparse_no_traffic_data:
            sparse_no_traffic_data.append(i)
    for i in std:
        if i not in sparse_traffic_data:
            sparse_traffic_data.append(i)
    # for i in sparse_no_traffic_data:
    #    print(i)
    #{'time': '2021-04-14T06:51:38.126000Z', 'source': 'ASR-9904-G-LS', 'group_address': '225.1.1.1', 'source_address': '0.0.0.0', 'rp_address/ipv4_address': '124.124.124.124', 'protocol': 'sm', 'rpt': '1', 'rpf_interface_name': 'HundredGigE0/0/0/8', 'rpf_neighbor/ipv4_address': '192.184.163.18', 'outgoing_interface/interface_name': 'HundredGigE0/0/0/10', 'alive': -1, 'last_hop': 'true'}
    
    # print(sparse_no_traffic_data)
    sparse_no_traffic_result=[]
    sparse_no_traffic_ans={}
    for i in sparse_no_traffic_data:
        for j in igmp_result:
            if i['source']==j['IGMP Neighbor'] and i['outgoing_interface/interface_name']==j['IGMP Neighbor Interface']:
                sparse_no_traffic_ans['source']=j['IGMP Source']
                sparse_no_traffic_ans['target']=j['IGMP Neighbor']
                sparse_no_traffic_ans['group']=i['group_address']
                sparse_no_traffic_ans['traffic']='0'
                #[traffic] is a flag value which tells whether traffic is there or not(P.S - For Visualization purpose)
                sparse_no_traffic_result.append(sparse_no_traffic_ans)
                sparse_no_traffic_ans={}

    for i in sparse_no_traffic_data:
        for j in pim_topology:
            if i['source']==j['Neighbor Name'] and i['rpf_interface_name']==j['Neighbor Interface']:
                sparse_no_traffic_ans['source']=j['Source Name']
                sparse_no_traffic_ans['target']=j['Neighbor Name']
                sparse_no_traffic_ans['group']=i['group_address']
                sparse_no_traffic_ans['traffic']='0'
                sparse_no_traffic_result.append(sparse_no_traffic_ans)
                sparse_no_traffic_ans={}

    for i in sparse_no_traffic_data:
        if i['rpf_interface_name']!= None:
            # print(i['rpf_interface_name'])
            if i['rpf_interface_name'].startswith('Decapstunnel') and i['rp_address/ipv4_address']==i['rpf_neighbor/ipv4_address'] :
                sparse_no_traffic_ans['source']= i['source']
                sparse_no_traffic_ans['target']= i['source']
                sparse_no_traffic_ans['group']=i['group_address']
                sparse_no_traffic_ans['traffic']='0'
                sparse_no_traffic_result.append(sparse_no_traffic_ans)
                sparse_no_traffic_ans={}

    sparse_traffic_result=[]
    sparse_traffic_ans={}
    for i in sparse_traffic_data:
        for j in igmp_result:
            if i['source']==j['IGMP Neighbor'] and i['outgoing_interface/interface_name']==j['IGMP Neighbor Interface']:
                sparse_traffic_ans['source']=j['IGMP Source']
                sparse_traffic_ans['target']=j['IGMP Neighbor']
                sparse_traffic_ans['group']=i['group_address']
                sparse_traffic_ans['traffic']='1'
                sparse_traffic_result.append(sparse_traffic_ans)
                sparse_traffic_ans={}

    for i in sparse_traffic_data:
        for j in pim_topology:
            if i['source']==j['Neighbor Name'] and i['rpf_interface_name']==j['Neighbor Interface']:
                sparse_traffic_ans['source']=j['Source Name']
                sparse_traffic_ans['target']=j['Neighbor Name']
                sparse_traffic_ans['group']=i['group_address']
                sparse_traffic_ans['traffic']='1'
                sparse_traffic_result.append(sparse_traffic_ans)
                sparse_traffic_ans={}

    for i in sparse_traffic_data:
        if i['rpf_interface_name']!= None:
            if i['rpf_interface_name'].startswith('Decapstunnel') and i['rp_address/ipv4_address']==i['rpf_neighbor/ipv4_address'] :
                sparse_traffic_ans['source']= i['source']
                sparse_traffic_ans['target']= i['source']
                sparse_traffic_ans['group']=i['group_address']
                sparse_traffic_ans['traffic']='1'
                sparse_traffic_result.append(sparse_traffic_ans)
                sparse_traffic_ans={}

    #Filtering the repeated values
    final_sparse_no_traffic_result=[]
    for i in sparse_no_traffic_result:
        if i not in final_sparse_no_traffic_result:
            final_sparse_no_traffic_result.append(i)

    #Adding the none group
    nonegroup={}
    for i in total_source_target:
        # if not i['target'].startswith('Multicast'):
        nonegroup['source']=i['source']
        nonegroup['target']=i['target']
        nonegroup['group']='None'
        nonegroup['traffic']='0'
        final_sparse_no_traffic_result.append(nonegroup)
        nonegroup={}

    #Filtering the repeated values
    final_sparse_traffic_result=[]
    for i in sparse_traffic_result:
        if i not in final_sparse_traffic_result:
            final_sparse_traffic_result.append(i)

    #Adding the none group
    if(len(final_sparse_traffic_result)!=0):
        nonegroup={}
        for i in total_source_target:
            # if not i['target'].startswith('Multicast'):
            nonegroup['source']=i['source']
            nonegroup['target']=i['target']
            nonegroup['group']='None'
            nonegroup['traffic']='1'
            final_sparse_traffic_result.append(nonegroup)
            nonegroup={}

    #Groups list when there is no traffic
    sm_groups=[]
    for i in final_sparse_no_traffic_result:
        if i['group'] not in sm_groups:
            sm_groups.append(i['group'])

    #Groups list when there is traffic
    if(len(final_sparse_traffic_result)!=0):
        sm_groups=[]
        for i in final_sparse_traffic_result:
            if i['group'] not in sm_groups:
                sm_groups.append(i['group'])

    #Finding the rp router
    for i in final_sparse_no_traffic_result:
        if i['source']==i['target']:
            rp_router=i['source']

    #Finding the rp router
    for i in final_sparse_traffic_result:
        if i['source']==i['target']:
            rp_router=i['source']

    # Combining with and without traffic for visualization purpose and deleting the repeated source and targets.
    if(len(final_sparse_traffic_result)!=0):
        for i in final_sparse_traffic_result:
            for j in final_sparse_no_traffic_result:
                if((i['source']==j['source'] and i['target']==j['target'] and i['group']!='None' and j['group']!='None')or((i['source']==j['target'])and(i['target']==j['source'])and i['group']!='None' and j['group']!='None')):
                    # print(i['source'],j['source'])
                    final_sparse_no_traffic_result.remove(j)
        final_sparse_traffic_result.extend(final_sparse_no_traffic_result)

    print(sm_groups)
    # print(final_sparse_no_traffic_result)
    # print(final_sparse_traffic_result)
    # final_sparse_traffic_result=[]
    return final_sparse_traffic_result,final_sparse_no_traffic_result,sm_groups,rp_router