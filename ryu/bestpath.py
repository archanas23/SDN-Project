import logging
import random
from webob import Response
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import *
from ryu.ofproto import ether
from ryu.lib import *
from pprint import pprint
from ryu.app.wsgi import ControllerBase, WSGIApplication
from ryu.app import simple_switch
import json 
from ryu.topology.api import get_link
from ryu.lib import dpid as dpid_lib
import struct
from ryu.lib import port_no as port_lib
from ryu.lib.mac import haddr_to_bin
from ryu.lib.ip import ipv4_to_bin
from ryu.lib import addrconv
import networkx as nx
import re

class ShortestPath(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(ShortestPath, self).__init__(req, link, data, **config)
        self.dpset = data['dpset']
        self.waiters = data['waiters']
        self.topology_api_app = data['linkapi']
	  
    def shortest_route(self,src,dst):
        Grf=nx.Graph()
        file_1=open("//home//archanas//ryu//link_add.txt",'r')
        point_1=re.compile("dpid=\d+")
        for data in file_1:
            str_1=re.findall(point_1,data)
            Grf.add_node(str_1[0])
            Grf.add_node(str_1[1])
            Grf.add_edge(str_1[0],str_1[1],weight=random.randrange(300,401))
	   
        return nx.shortest_path(Grf,"dpid="+str(src),"dpid="+str(dst))
    
    def append(self,dpid):
        dpid=str(dpid)
        length=16-len(dpid)
	return str(0)*length+dpid

    
    def push_flow(self, req, source_dpid_int, destn_dpid_int, mac, **_kwargs):
        path = self.shortest_route(source_dpid_int, destn_dpid_int)

        source_dpid = self.append(source_dpid_int)
        destn_dpid = self.append(destn_dpid_int)
	source_dpid1 = dpid_lib.str_to_dpid(source_dpid)
        destn_dpid1 = dpid_lib.str_to_dpid(destn_dpid)
        source_dp = self.dpset.get(source_dpid1)
        destn_dp = self.dpset.get(destn_dpid1)
	 
        if source_dp is None:
		return Response(status=404)
            
        for node in range(len(path)-1):
            tsrc_dpid = int(path[node].replace("dpid=",""))
            tdst_dpid = int(path[node+1].replace("dpid=",""))
            tsrc_dpid = self.append(tsrc_dpid)
            tdst_dpid = self.append(tdst_dpid)
            tsrc_dpid = dpid_lib.str_to_dpid(tsrc_dpid)
            tdst_dpid = dpid_lib.str_to_dpid(tdst_dpid)
            tsrc_dp = self.dpset.get(tsrc_dpid)
	   
            links = get_link(self.topology_api_app, tsrc_dpid)
		
            if links is None:
                return Response(status=404)            
            for i in range(len(links)):
                links_dpid = dpid_lib.str_to_dpid(links[i].to_dict()["dst"]["dpid"])
                if links_dpid == tdst_dpid:
                    str_port = links[i].to_dict()["src"]["port_no"]  
                    break            
            port = port_lib.str_to_port_no(str_port)
            actions = [tsrc_dp.ofproto_parser.OFPActionOutput(int(port))]
            # pushing flows
            ofproto = tsrc_dp.ofproto
            
            match = tsrc_dp.ofproto_parser.OFPMatch(dl_dst=haddr_to_bin(mac))
            mod = tsrc_dp.ofproto_parser.OFPFlowMod(
                datapath=tsrc_dp, match=match, cookie=0,
                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                priority=ofproto.OFP_DEFAULT_PRIORITY,
                flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
            tsrc_dp.send_msg(mod)

        
        ofproto = destn_dp.ofproto
       
        if(destn_dpid1 == 0000000000000001):
            logging.debug("PORT")
            out_port = 1
            logging.debug(out_port)
            logging.debug("PORT")
        if(destn_dpid1 == 0000000000000002):
            out_port = 3
        if(destn_dpid1 == 0000000000000003):
            out_port = 2
        actions1 = [destn_dp.ofproto_parser.OFPActionOutput(1)]
        match1 = destn_dp.ofproto_parser.OFPMatch(dl_dst=haddr_to_bin(mac))
       
        mod1 = destn_dp.ofproto_parser.OFPFlowMod(
            datapath=destn_dp, match=match1, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions1)
        destn_dp.send_msg(mod1)
	
        body = json.dumps([link.to_dict() for link in links])
        return Response(content_type='application/json', body=body)


class RestPathApi(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION,
                    ofproto_v1_2.OFP_VERSION,
                    ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {
        'dpset': dpset.DPSet,
        'wsgi': WSGIApplication
    }

    def __init__(self, *args, **kwargs):
        super(RestPathApi, self).__init__(*args, **kwargs)
        self.dpset = kwargs['dpset']
        self.linkapi = self
        wsgi = kwargs['wsgi']
        self.waiters = {}
        self.data = {}
        self.data['dpset'] = self.dpset
        self.data['waiters'] = self.waiters
        self.data['linkapi'] = self.linkapi
        mapper = wsgi.mapper

        wsgi.registory['ShortestPath'] = self.data
        
        
        uri = '/v1.0/topology/transfer_flows/{source_dpid_int}/{destn_dpid_int}/{mac}'
        mapper.connect('bestpath', uri,
                       controller=ShortestPath,action='push_flow',
                       conditions=dict(method=['GET']))
