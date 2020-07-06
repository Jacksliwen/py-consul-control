# -*- coding:utf-8 -*-
#注销该集群下所有不可用节点
import requests
import json
import sys

#获取集群下所有机器ip
ip = '127.0.0.1'
if len(sys.argv[1]) != 0:
    ip = sys.argv[1]
url = 'http://'+ ip +':8500/v1/agent/members'
req = requests.get(url)
res = json.loads(req.content)


#res保存所有ip,循环注销该ip下所有不可用节点
for each in res:
    #print(each["Addr"])
    #获取每个节点下所有服务id
    each_url = 'http://'+ each["Addr"] +':8500/v1/agent/checks'
    req = requests.get(each_url)
    each_res = json.loads(req.content)
    for each_service in each_res:
        if each_res[each_service]["Status"] == "critical":
            url = 'http://'+ each["Addr"] + ':8500/v1/agent/service/deregister/' + each_res[each_service]["ServiceID"]
            req = requests.put(url)
            print(each["Addr"] + " deregister [ " + each_res[each_service]["ServiceID"] + " ] ")