def makeTopology(pim_data,igmp_data):
    local_pim_table = []
    neighbor_pim_table = []
    pim_results=[]

    for i in pim_data:
        for j in i:
            for k,v in j.items():
                if k == 'IP' and v.startswith("192.184.163"):
                    pim_results.append(j)

    for i in pim_results:
        if i['is_this_neighbor_us'] == 'true' :
            local_pim_table.append(i)
        elif i['is_this_neighbor_us'] == 'false' :
            neighbor_pim_table.append(i)

    if len(local_pim_table)==len(neighbor_pim_table):
        print("Data Consistent. Good to Go!")
    else :
        print("Data Inconsistent. Trying to work with the consistent subset ......")

    # print(neighbor_pim_table)
    # print(local_pim_table)
    pim_ans={}
    pim_res=[]
    for i in neighbor_pim_table:
        for j in local_pim_table:
            if i['IP']==j['IP']:
                pim_ans['Neighbor IP']= i['IP']
                pim_ans['Neighbor Name']=j['source']
                pim_ans['Neighbor Interface']=j['interface_name']
            if i['source']==j['source'] and i['interface_name']==j['interface_name']:
                pim_ans['Source IP']=j['IP']
                pim_ans['Source Name']=i['source']
                pim_ans['Source Interface']=i['interface_name']
        pim_res.append(pim_ans)
        pim_ans={}
    # print(pim_res)
    result=[]
    for i in pim_res:
        if len(i)==6:
            result.append(i)        
    #prints all results (6 key-value pairs)
    # print(result)

    pim_routers=[]
    for i in result:
        if {'id':i['Source Name']} not in pim_routers:
            pim_routers.append({'id':i['Source Name']})
    #print(pim_routers)  #prints routers name in pim topology

    pim_source_target=[]
    kv={}
    for i in result:
        kv['source']=i['Source Name']
        kv['target']=i['Neighbor Name']
        pim_source_target.append(kv)
        kv={}
    
    pim_topology=list(result)
    total_routers=list(pim_routers)
    total_source_target=list(pim_source_target)

    #IGMP
    igmp_result=[]
    igmp_ans={}
    x=1
    for j in igmp_data:
        for i in j:
            igmp_ans['IGMP Neighbor']=i['source']
            igmp_ans['IGMP Neighbor Interface']=i['interface_name']
            igmp_ans['IGMP Source IP']=i['last_reporter/ipv4_address']
            igmp_ans['Group Address']=i['group_address']
            igmp_ans['IGMP Source'] = "Receiver "+ str(x) 
        x=x+1
        igmp_result.append(igmp_ans)
        igmp_ans={}
    
    igmp_kv={}
    for i in igmp_result:
        igmp_kv['source']=i['IGMP Source']
        igmp_kv['target']=i['IGMP Neighbor']
        total_source_target.append(igmp_kv)
        igmp_kv={}

    for i in igmp_result:
        if {'id':i['IGMP Source']} not in total_routers:
            total_routers.append({'id':i['IGMP Source']})

    for i in igmp_result:
        if i not in result:
            result.append(i)

    topology=list(result)

    return topology,total_routers,total_source_target,igmp_result,pim_topology