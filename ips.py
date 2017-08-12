import sys
import os
import httplib
import json

class StaticEntryPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret
    
controller_ip=sys.argv[1]

pusher = StaticEntryPusher(controller_ip)
name=1
with open('alertlogs.txt', 'r') as fp:
    data=fp.read()
    for entry in data.split('\n'):
        #print entry
        chunk=entry.split()
        print chunk
        
        
        proto=chunk[9]
        proto=proto[1:]
        proto=proto[:-1]
        print proto
        if proto!="ICMP":
            src_ip_data=chunk[10]
            src_ip=src_ip_data.split(':')[0]
            dst_ip_data=chunk[12]
            dst_ip=dst_ip_data.split(':')[0]
        else:
            src_ip=chunk[10]
            dst_ip=chunk[12]
        print src_ip
        print dst_ip
        if proto=="ICMP":
            flow1 = {
                'switch':"00:00:00:00:00:00:00:01",
                "name":name,
                "cookie":"0",
                "priority":"25000",
                "eth_type":"0x0800",
                "ip_proto":"0x01",
                "ipv4_src": src_ip,
                "ipv4_dst": dst_ip,
                "hard_timeout":"10",
                "active":"true"
            }
            pusher.set(flow1)
            name +=1
        elif proto=="TCP":
            flow1 = {
                'switch':"00:00:00:00:00:00:00:01",
                "name":name,
                "cookie":"0",
                "priority":"25000",
                "eth_type":"0x0800",
                "ip_proto":"0x06",
                "ipv4_src": src_ip,
                "ipv4_dst": dst_ip,
                "hard_timeout":"10",
                "active":"true"
            } 
            pusher.set(flow1)
            name +=1
        else:
            pass
        break
print"Exiting"
sys.exit()
