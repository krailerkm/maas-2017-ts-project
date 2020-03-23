#!/usr/bin/env python
################# Include Module #################
import keystoneclient.v2_0.client as keyclient          #Openstack SDK Module Keystore
import neutronclient.v2_0.client as netclient           #Openstack SDK Module Neutron
import novaclient.v2.client as novaclient               #Openstack SDK Module Nova
import ceilometerclient.v2.client as ceioclient         #Openstack SDK Module Ceilometerclient
import heatclient.v1.client as heatclient               #Openstack SDK Module Heat
import glanceclient.v2.client as glanceclient           #Openstack SDK Module Glance
import datetime as timeclient                           #Basic Module Date and Time
import time as sleep                                    #Basic Module Time sleep
import credentials as credentialsclient                 #Crafted Store Openstack User & Password    (MY Create)
import json                                             #Json format for API Get
import pycurl                                           #Curl for API Get
import cStringIO                                        #cStringIO for Open Socket
import socket                                           #Open Socket
import uuid                                             #UUIDs objects according to RFC 4122

try:
################# Keystone Authentication #################
    credentials = credentialsclient.get_credentials()       #Define parameter username and password from crafted module
    keystone = keyclient.Client(**credentials)              #Define parameter and get token from Keystore module
################# Nova Authentication #################
    nova = novaclient.client.Client(2,username=keystone.username,password=keystone.password,project_id=keystone.project_id,auth_url=keystone.auth_url)
################# Neutron Authentication #################
    net_endpoint = keystone.service_catalog.url_for(service_type='network')             #Get endpoint service of Neutron
    neutron = netclient.Client(endpoint_url=net_endpoint ,token=keystone.auth_token)    #Authentication Neutron by endpoint and token
################# Ceilometer Authentication #################
    ceio_endpoint = keystone.service_catalog.url_for(service_type='metering')           #Get endpoint service of Ceilometerclient
    ceio = ceioclient.Client(endpoint=ceio_endpoint ,token=keystone.auth_token)         #Authentication Ceilometerclient by endpoint and token
################# Ceilometer Alarm Authentication #################
    alarm_endpoint = keystone.service_catalog.url_for(service_type='alarming')          #Get endpoint service of Alarm
    alarmc = ceioclient.Client(endpoint=alarm_endpoint ,token=keystone.auth_token)      #Authentication Alarm by endpoint and token
################# Heat Authentication #################
    heat_endpoint=keystone.service_catalog.url_for(service_type='orchestration')        #Get endpoint service of Heat
    heatc=heatclient.Client("1", heat_endpoint, token=keystone.tokens)         #Authentication Heat by endpoint and token
################# Heat Authentication #################
    glance_endpoint=keystone.service_catalog.url_for(service_type='image')        #Get endpoint service of glance
    glancec=glanceclient.Client(endpoint=glance_endpoint ,token=keystone.auth_token)         #Authentication glace by endpoint and token
    print "Online Mode connectted controller server"  # Print after can't connect
except:
    print "!!Offline Mode can't connect controller server!!"  # Print after can't connect
################# Create Pool #################
def create_pool(subnet_id=str(), lb_method="LEAST_CONNECTIONS", protocol="HTTP", name="API-POOL", admin_state_up=True):
    try:
        body_sample = {"pool": {"subnet_id": subnet_id, "lb_method": lb_method, "protocol": protocol, "name": name, "admin_state_up": admin_state_up}} #Body define parameter from debug Neutron command-line Client
        pool_return = neutron.create_pool(body=body_sample) #Create pool load balance and get return parameter
        id_pool = pool_return.get('pool')['id']             #Get new id pool created for delete in next time
        print timeclient.datetime.today(), "Create Pool:", id_pool  #Print Task detial
        return pool_return                                  #Return create
    except:
        print timeclient.datetime.today(), "Error Can't Create Pool"    #Print after cteate complete
################# List Pool #################
def list_pool():
    try:
        list_pool_return=neutron.list_pools()
        tmp_pool_list_return=list()
        for tmp_pool_return in list_pool_return.get('pools'):
            tmp_pool_list_return.append(str(tmp_pool_return["id"]))
        if tmp_pool_list_return==list():  #If not list value
            tmp_pool_list_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List all Pool:", tmp_pool_list_return #Print Task detial
        return list_pool_return                                  #Return create
    except:
        print timeclient.datetime.today(), "Error Can't List all Pool"    #Print after List complete
################# Delete Pool #################
def delete_pool(id_pool=str()):
    try:
        delete_pool_return=neutron.delete_pool(pool=id_pool)
        print timeclient.datetime.today(), "Delete Pool:", id_pool    #Print after delete complete
        return delete_pool_return  #Return Delete
    except:
        print timeclient.datetime.today(), "Error Can't Delete Pool"    #Print after delete complete
################# Create VM #################
def create_vm(image_name="cirros", flavors_name="m1.tiny", network_name="private", meta_name="API-DATA", vm_name="vm1"):
    try:
        image_id = nova.images.find(name=image_name)
        #images_return = glancec.images.list()
        #for tmp_glance_list in images_return:
            #if image_name == str(tmp_glance_list.get("name")):
                #print tmp_glance_list.get("id")
                #image_id = str(tmp_glance_list.get("id"))
        flavor = nova.flavors.find(name=flavors_name)
        net = nova.networks.find(label=network_name)
        nics = [{'net-id': net.id}]
        metad = {'metering.stack': meta_name}
        nova_return = nova.servers.create(name=vm_name, image=image_id, flavor=flavor, nics=nics, meta=metad)
        print timeclient.datetime.today(), "Create VM:", nova_return.name, nova_return.id   #Print Task detial
        return nova_return.name  #Return Create
    except:
            print timeclient.datetime.today(), "Error Can't Create VM"  # Print after create vm
################# Sleep time for create VM #################
def sleep_status_vm(name=str(),time_out=int()):
    try:
        tmp_status=True   #Status for exit loop
        tmp_find_vm=str()   #Find VM
        tmp_count_time=0    #count time
        while (tmp_status): #Run any time
            tmp_list_vm_return=nova.servers.list()  #List all vm
            for tmp_server in tmp_list_vm_return:   #Select 1 of all vm
                if tmp_server.name==name:   #Select vm same name parameter
                    tmp_find_vm=tmp_server.name
                    if tmp_server.status == "BUILD":    #If status build sleep 1s
                        sleep.sleep(1)  #sleep 1s
                        tmp_count_time=tmp_count_time+1   #count time 1s
                    elif tmp_server.status == "ACTIVE":   #If status active for exit
                        tmp_status = False  #Exit
                        print timeclient.datetime.today(), "Status VM Complete:", tmp_server.name, tmp_server.status, "in", tmp_count_time, "sec."  #
            if len(tmp_list_vm_return)==0 or tmp_find_vm==str():
                tmp_status = False  # Exit
                print timeclient.datetime.today(), "Don't have VM:", name
            elif tmp_count_time==time_out:
                tmp_status = False  # Exit
                print timeclient.datetime.today(), "Time out VM:", name, "in", time_out, "sec."
    except:
        print timeclient.datetime.today(), "Error Can't Sleep Status VM"
################# List VM #################
def list_vm():
    try:
        list_vm_return = nova.servers.list()
        tmp_vm_list_return = list()
        for tmp_vm_list in list_vm_return:
            tmp_vm_list_return.append(str(tmp_vm_list.name))
        if tmp_vm_list_return==list():  #If not list value
            tmp_vm_list_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List all VM:", tmp_vm_list_return
        return list_vm_return
    except:
        print timeclient.datetime.today(), "Error Can't List all VM"  # Print after list vm
################# Delete VM #################
def delete_vm(vm_name=str()):
    try:
        for tmp_server in nova.servers.list():
            if tmp_server.name == vm_name:
                delete_vm_return = nova.servers.delete(tmp_server)
                print timeclient.datetime.today(), "Delete VM:", tmp_server.name, tmp_server.id
                return tmp_server.name  # Return Delete
        print timeclient.datetime.today(), "Not exist VM:", vm_name #if not found vm for delete
    except:
        print timeclient.datetime.today(), "Error Can't Delete VM"  # Print after delete vm
################# Show IP VM #################
def show_ip_vm(vm_name=str()):
    try:
        server_exists = nova.servers.find(name=vm_name)
        ip_server = server_exists.addresses['private'][0]['addr']
        print timeclient.datetime.today(), "Show VM:", server_exists.id, "IP:", ip_server
        return ip_server
    except:
        print timeclient.datetime.today(), "Error Can't Show VM IP"  # Print after show IP VM
################# Create Health Monitor #################
def create_health_monitor(delay="1", max_retries="1", type="HTTP", timeout="1", admin_state_up=True):
    try:
        body_sample = {"health_monitor": {"delay": delay, "max_retries": max_retries, "type": type, "timeout": timeout, "admin_state_up": admin_state_up}}
        mon_return = neutron.create_health_monitor(body=body_sample)
        print timeclient.datetime.today(), "Create Health Monitor:", mon_return.get("health_monitor")['id']   #Print Task detial
        return mon_return
    except:
        print timeclient.datetime.today(), "Error Can't Create Health Monitor"  # Enable Health Monitor VIP
################# Associate Health Monitor #################
def associate_health_monitor(pool=str(), health_monitor=str()):
    try:
        if health_monitor == str():
            print timeclient.datetime.today(), "Not exist Health Monitor:", health_monitor
        if pool == str():
            print timeclient.datetime.today(), "Not exist Pool:", pool
        else:
            body_sample = {"health_monitor": {"id": health_monitor}}
            health_monitor_return = neutron.associate_health_monitor(pool=pool,body=body_sample)
            print timeclient.datetime.today(), "Associate Health Monitor:", health_monitor, "Pool:", pool  # Print after Associate Health Monitor VIP
            return health_monitor_return
    except:
        print timeclient.datetime.today(), "Error Can't Associate Health Monitor"  # Print after Associate Health Monitor VIP
################# List Health Monitor #################
def list_health_monitors():
    try:
        list_hralth_return=neutron.list_health_monitors()
        tmp_list_hralth_return = list() #list all health monitors
        for tmp_hralth_list in list_hralth_return.get('health_monitors'):
            tmp_list_hralth_return.append(str(tmp_hralth_list["id"]))   #find list health monitors
        if tmp_list_hralth_return==list():  #If not list value
            tmp_list_hralth_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List all Health Monitor:", tmp_list_hralth_return  # Print after List all Health Monitor VIP
        return list_hralth_return
    except:
        print timeclient.datetime.today(), "Error Can't List all Health Monitor"  # Print after List all Health Monitor VIP
################# Disassociate Health Monitor #################
def dissociate_health_monitor(pool=str(), health_monitor=str()):
    try:
        if health_monitor == str():
            print timeclient.datetime.today(), "Not exist Health Monitor:", health_monitor
        if pool == str():
            print timeclient.datetime.today(), "Not exist Pool:", pool
        else:
            health_monitor_return = neutron.disassociate_health_monitor(pool=pool,health_monitor=health_monitor)
            print timeclient.datetime.today(), "Disassociate Health Monitor:", health_monitor, "Pool:", pool # Print after Disassociate Health Monitor VIP
            return health_monitor_return
    except:
        print timeclient.datetime.today(), "Error Can't Disassociate Health Monitor"  # Print after Disassociate Health Monitor VIP
################# Delete Health Monitor #################
def  delete_health_monitor(health_monitor=str()):
    try:
        delete_health_monitor_return=neutron.delete_health_monitor(health_monitor=health_monitor)
        print timeclient.datetime.today(), "Delete Health Monitor:", health_monitor  # Print after delete Health Monitor VIP
        return delete_health_monitor_return
    except:
        print timeclient.datetime.today(), "Error Can't Delete Health Monitor"  # Print after Delete Health Monitor VIP
################# Add VIP #################
def create_vip(protocol="HTTP",name_vip_pool="API-VIP",admin_state_up=True,subnet_id=str(),pool_id=str(),protocol_port="80"):
    try:
        body_sample = {"vip": {"protocol": protocol, "name": name_vip_pool, "admin_state_up": admin_state_up, "subnet_id": subnet_id, "pool_id": pool_id, "protocol_port": protocol_port}}
        vip_return = neutron.create_vip(body=body_sample)
        print timeclient.datetime.today(), "Create VIP:", vip_return.get("vip")['id']  # Print after Add Pool VIP
        return vip_return
    except:
        print timeclient.datetime.today(), "Error Can't Create VIP"  # Print after Add Pool VIP
################# List VIP #################
def list_vip():
    try:
        list_vip_return=neutron.list_vips()
        tmp_list_vip_return = list()
        for tmp_list_vip in list_vip_return.get('vips'):
            tmp_list_vip_return.append(str(tmp_list_vip["id"]))
        if tmp_list_vip_return==list():  #If not list value
            tmp_list_vip_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List all VIP:", tmp_list_vip_return  # Print after list all VIP
        return list_vip_return
    except:
        print timeclient.datetime.today(), "Error Can't List all VIP"  # Print after list all VIP
################# Delete VIP #################
def delete_vip(vip=str()):
    try:
        delete_vip_return=neutron.delete_vip(vip=vip)
        print timeclient.datetime.today(), "Delete VIP:", vip # Print after delete Pool VIP
        return delete_vip_return
    except:
        print timeclient.datetime.today(), "Error Can't Delete VIP"  # Print after delete Pool VIP
################# Create Floating #################
def create_floating(floating_network_id=str()):
    try:
        body_sample = {"floatingip": {"floating_network_id": floating_network_id}}
        create_floatingip_return = neutron.create_floatingip(body=body_sample)
        print timeclient.datetime.today(), "Create Floating:", create_floatingip_return.get("floatingip")['id'] # Print after Create Floating IP
        return create_floatingip_return
    except:
        print timeclient.datetime.today(), "Error Can't Create Floating"  # Print after Create Floating IP
################# Associate Floating #################
def associate_floating(port_id=str(),floating_id=str()):
    try:
        body_sample = {"floatingip": {"port_id": port_id}}
        associate_floatingip_return = neutron.update_floatingip(floatingip=floating_id,body=body_sample)
        print timeclient.datetime.today(), "Associate Floating:", floating_id, "Port:", port_id  # Print after Associate Floating
        return associate_floatingip_return
    except:
        print timeclient.datetime.today(), "Error Can't Associate Floating"  # Print after Associate Floating
################# List Floating #################
def list_floating():
    try:
        list_floating_return = neutron.list_floatingips()
        tmp_list_floating_return = list()
        for tmp_list_floating in list_floating_return.get('floatingips'):
            tmp_list_floating_return.append(str(tmp_list_floating["id"]))
        if tmp_list_floating_return==list():  #If not list value
            tmp_list_floating_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List all Floating:", tmp_list_floating_return  # Print after List all Floating
        return list_floating_return
    except:
        print timeclient.datetime.today(), "Error Can't List all Floating"  # Print List all Floating
################# Delete Floating #################
def delete_floating(floatingip=str()):
    try:
        delete_floating_return=neutron.delete_floatingip(floatingip=floatingip)
        print timeclient.datetime.today(), "Delete Floating:", floatingip  # Print after Delete Floating
        return delete_floating_return
    except:
        print timeclient.datetime.today(), "Error Can't Delete Floating"  # Print Delete Floating
################# Create Member #################
def create_member(weight=1,protocol_port="80",address=str(),pool_id=str(),admin_state_up=True):
    try:
        body_sample = {"member": {"weight":weight,"protocol_port": protocol_port, "address": address, "pool_id": pool_id, "admin_state_up": admin_state_up}}
        lb_member_return = neutron.create_member(body=body_sample)
        print timeclient.datetime.today(), "Create Member:", lb_member_return.get("member")['id']  # Print after Create Member Load Balance
        return lb_member_return
    except:
        print timeclient.datetime.today(), "Error Can't Create Member"  # Print after Create Member
################# List Member #################
def list_member():
    try:
        list_member_return = neutron.list_members()
        tmp_list_member_return = list()
        for tmp_list_member in list_member_return.get('members'):
            tmp_list_member_return.append(str(tmp_list_member["id"]))
        if tmp_list_member_return==list():  #If not list value
            tmp_list_member_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List Member:", tmp_list_member_return
        return list_member_return
    except:
        print timeclient.datetime.today(), "Error Can't List Member"  # Print after List Member
################# Delete Member #################
def delete_member(member=str()):
    try:
        lb_member_return = neutron.delete_member(member=member)
        print timeclient.datetime.today(), "Delete Member:", member
        return lb_member_return
    except:
        print timeclient.datetime.today(), "Error Can't Delete Member"  # Print after Delete Member Load Balance
################# Create Alarm by API #################
def create_alarm(alarm_actions="log://",description="instance running hot",meter_name="cpu_util",evaluation_periods=3,period=600,statistic="avg",threshold=15.0,field="metadata.user_metadata.stack",value="API-DATA",op="eq",comparison_operator="lt",repeat_actions=True,type="threshold",name="cpu_low"):
    try:
        buf = cStringIO.StringIO()  #Create buffer string IO
        tmp_token = "X-Auth-Token: " + keystone.auth_token    #Define token for authen alarms service
        data = json.dumps({"alarm_actions": [alarm_actions], "description": description, "threshold_rule": {"meter_name": meter_name, "evaluation_periods": evaluation_periods, "period": period, "statistic": statistic, "threshold": threshold, "query": [{"field": field, "value": value, "op": op}], "comparison_operator": comparison_operator}, "repeat_actions": repeat_actions, "type": type, "name": name})
        c = pycurl.Curl()   #Open CURL
        c.setopt(c.URL, str(alarm_endpoint+"/v2/alarms"))    #Define alarm endpoint
        c.setopt(c.HTTPHEADER, ['User-Agent: ceilometerclient.openstack.common.apiclient', 'Content-Type: application/json', str(tmp_token)])  #Create Type of parameter API
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        alarm_return_str = buf.getvalue()
        buf.close()
        alarm_return_str.replace("'", "\"") #Replace all ' to "
        alarm_return = json.loads(alarm_return_str) #Convert srt to dir
        print timeclient.datetime.today(), "Create Alarm:", alarm_return.get("name"), alarm_return.get("alarm_id")  #Show after Create Alarm
        return alarm_return
    except:
        print timeclient.datetime.today(), "Error Can't Create Alarm"  # Print after Create Alarm
################# List Alarm #################
def list_alarm():
    try:
        list_alarm_return = alarmc.alarms.list()
        tmp_list_alarm_return = list()
        for tmp_list_alarm in list_alarm_return:
            tmp_list_alarm_return.append(str(tmp_list_alarm.id))
        if tmp_list_alarm_return==list():  #If not list value
            tmp_list_alarm_return.append("Empty")  #Insert Empty to print
        print timeclient.datetime.today(), "List all Alarm:", tmp_list_alarm_return  # Print after List all Alarm
        return list_alarm_return
    except:
        print timeclient.datetime.today(), "Error Can't List all Alarm"  # Print after List all Alarm
################# Delete Alarm #################
def delete_alarm(alarm_id=str()):
    try:
        alarm_delete_return = alarmc.alarms.delete(alarm_id=alarm_id)
        print timeclient.datetime.today(), "Delete Alarm:", alarm_id   # Print after delete Alarm
        return alarm_delete_return
    except:
        print timeclient.datetime.today(), "Error Can't Delete Alarm ID:", alarm_id  # Print after delete Alarm
################# Opensocket Receive Alarm #################
def open_receive_alarm():
    try:
        HOST, PORT = '', 8888
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        print timeclient.datetime.today(), "Wait for Receive Alarm Action...."
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        tmp_split_rn = request.split('\r\n')    #split new line
        tmp_split_action = tmp_split_rn[0].split()  #split first line for find action
        if tmp_split_action[1] == '/high-cpu':
            print timeclient.datetime.today(), "Receive Alarm High CPU"
            http_response = "HTTP/1.1 200 OK\n\nCPU HIGH!"
            client_connection.sendall(http_response)
            client_connection.close()
            return "high-cpu"
        elif tmp_split_action[1] == '/low-cpu':
            print timeclient.datetime.today(),"Receive Alarm Low CPU"
            http_response = "HTTP/1.1 200 OK\n\nCPU LOW!"
            client_connection.sendall(http_response)
            client_connection.close()
            return "low-cpu"
        else:
            print timeclient.datetime.today(),"Receive Other Request~!!"
            http_response = "HTTP/1.1 200 OK\n\nHello, World!"
            client_connection.sendall(http_response)
            client_connection.close()
            return "Other"
    except:
        print timeclient.datetime.today(),"Error Can't Wait for Receive Alarm"  # Print after Sniff Alarm
################# Show IP Command Server Receive Alarm #################
def show_command_server_ip(detail=str()):
    try:
        server_ip = socket.gethostbyname(socket.gethostname())
        print timeclient.datetime.today(), "Command Server IP:", server_ip, detail  #Show IP Server Check Alarm
        return server_ip
    except:
        print timeclient.datetime.today(), "Error Can't Command Server" # Show IP Server Check Alarm
################# Print Sub Network #################
def find_subnet_id(name=str()):
    try:
        tmp_list = neutron.list_subnets()
        for tmp in tmp_list['subnets']:
            if name == tmp['name']:
                print timeclient.datetime.today(), "Find Subnet:", tmp['name'], tmp['id']  # Show Network ID
                return tmp['id']
    except:
        print timeclient.datetime.today(), "Find Subnet:", tmp['name'], tmp['id']  # Show Network ID
################# Find Network ID #################
def find_network_id(name=str()):
    try:
        tmp_network_list = neutron.list_networks()
        #print tmp_network_list
        for tmp_network in tmp_network_list['networks']:
            if name == tmp_network['name']:
                print timeclient.datetime.today(), "Find Network:", tmp_network['name'], tmp_network['id']  # Show Network ID
                return tmp_network['id']
    except:
        print timeclient.datetime.today(), "Find Subnet:", tmp_network['name'], tmp_network['id']  # Show Network ID
################# Create Stack Orchestration by API #################
def create_stack():
    try:
        buf = cStringIO.StringIO()  #Create buffer string IO
        tmp_token = "X-Auth-Token: " + keystone.auth_token    #Define token for authen heat service
        data = json.dumps({"files": {"file:///root/YML-SET2/server_lb.yaml": "{\"outputs\": {\"server_ip\": {\"description\": \"IP Address of the load-balanced server.\", \"value\": {\"get_attr\": [\"server\", \"first_address\"]}}, \"lb_member\": {\"description\": \"LB member details.\", \"value\": {\"get_attr\": [\"member\", \"show\"]}}}, \"heat_template_version\": \"2013-05-23\", \"description\": \"A load-balancer server\", \"parameters\": {\"image\": {\"type\": \"string\", \"description\": \"Image used for servers\"}, \"pool_id\": {\"type\": \"string\", \"description\": \"Pool to contact\"}, \"network\": {\"type\": \"string\", \"description\": \"Network used by the server\"}, \"flavor\": {\"type\": \"string\", \"description\": \"flavor used by the servers\"}, \"metadata\": {\"type\": \"json\"}}, \"resources\": {\"member\": {\"type\": \"OS::Neutron::PoolMember\", \"properties\": {\"protocol_port\": 80, \"pool_id\": {\"get_param\": \"pool_id\"}, \"address\": {\"get_attr\": [\"server\", \"first_address\"]}}}, \"server\": {\"type\": \"OS::Nova::Server\", \"properties\": {\"flavor\": {\"get_param\": \"flavor\"}, \"networks\": [{\"network\": {\"get_param\": \"network\"}}], \"image\": {\"get_param\": \"image\"}, \"metadata\": {\"get_param\": \"metadata\"}}}}}"}, "disable_rollback": True, "parameters": {}, "stack_name": "stack", "environment": {}, "template": {"outputs": {"pool_ip_address": {"description": "The IP address of the load balancing pool", "value": {"get_attr": ["pool", "vip", "address"]}}, "scale_dn_url": {"description": "This URL is the webhook to scale down the autoscaling group. You can invoke the scale-down operation by doing an HTTP POST to this URL; no body nor extra headers are needed.\n", "value": {"get_attr": ["web_server_scaledown_policy", "alarm_url"]}}, "scale_up_url": {"description": "This URL is the webhook to scale up the autoscaling group.  You can invoke the scale-up operation by doing an HTTP POST to this URL; no body nor extra headers are needed.\n", "value": {"get_attr": ["web_server_scaleup_policy", "alarm_url"]}}, "website_url": {"description": "This URL is the \"external\" URL that can be used to access the Wordpress site.\n", "value": {"str_replace": {"params": {"host": {"get_attr": ["lb_floating", "floating_ip_address"]}}, "template": "http://host/"}}}, "ceilometer_query": {"description": "This is a Ceilometer query for statistics on the cpu_util meter Samples about OS::Nova::Server instances in this stack.  The -q parameter selects Samples according to the subject's metadata. When a VM's metadata includes an item of the form metering.X=Y, the corresponding Ceilometer resource has a metadata item of the form user_metadata.X=Y and samples about resources so tagged can be queried with a Ceilometer query term of the form metadata.user_metadata.X=Y.  In this case the nested stacks give their VMs metadata that is passed as a nested stack parameter, and this stack passes a metadata of the form metering.stack=Y, where Y is this stack's ID.", "value": {"str_replace": {"params": {"stackval": {"get_param": "OS::stack_id"}}, "template": "ceilometer statistics -m cpu_util -q metadata.user_metadata.stack=stackval -p 30 -a avg\n"}}}}, "heat_template_version": "2013-05-23", "description": "AutoScaling By IBM", "parameters": {"subnet_id": {"default": "private", "type": "string", "description": "subnet on which the load balancer will be located"}, "external_network_id": {"default": "public", "type": "string", "description": "UUID of a Neutron external network"}, "image": {"default": "corec", "type": "string", "description": "Image used for servers"}, "flavor": {"default": "m1.tiny.s", "type": "string", "description": "flavor used by the web servers"}, "network": {"default": "private", "type": "string", "description": "Network used by the server"}}, "resources": {"lb": {"type": "OS::Neutron::LoadBalancer", "properties": {"protocol_port": 80, "pool_id": {"get_resource": "pool"}}}, "monitor": {"type": "OS::Neutron::HealthMonitor", "properties": {"delay": 1, "max_retries": 1, "type": "HTTP", "timeout": 1}}, "cpu_alarm_high": {"type": "OS::Ceilometer::Alarm", "properties": {"meter_name": "cpu_util", "alarm_actions": [{"get_attr": ["web_server_scaleup_policy", "alarm_url"]}], "description": "Scale-up if the average CPU > 70% for 1 minute", "matching_metadata": {"metadata.user_metadata.stack": {"get_param": "OS::stack_id"}}, "evaluation_periods": 1, "period": 30, "statistic": "avg", "threshold": 70, "comparison_operator": "gt"}}, "web_server_scaleup_policy": {"type": "OS::Heat::ScalingPolicy", "properties": {"auto_scaling_group_id": {"get_resource": "asg"}, "adjustment_type": "change_in_capacity", "scaling_adjustment": 1, "cooldown": 30}}, "cpu_alarm_low": {"type": "OS::Ceilometer::Alarm", "properties": {"meter_name": "cpu_util", "alarm_actions": [{"get_attr": ["web_server_scaledown_policy", "alarm_url"]}], "description": "Scale-down if the average CPU < 15% for 10 minutes", "matching_metadata": {"metadata.user_metadata.stack": {"get_param": "OS::stack_id"}}, "evaluation_periods": 1, "period": 30, "statistic": "avg", "threshold": 15, "comparison_operator": "lt"}}, "asg": {"type": "OS::Heat::AutoScalingGroup", "properties": {"min_size": 1, "resource": {"type": "file:///root/YML-SET2/server_lb.yaml", "properties": {"network": {"get_param": "network"}, "flavor": {"get_param": "flavor"}, "pool_id": {"get_resource": "pool"}, "image": {"get_param": "image"}, "metadata": {"metering.stack": {"get_param": "OS::stack_id"}}}}, "max_size": 3}}, "lb_floating": {"type": "OS::Neutron::FloatingIP", "properties": {"floating_network_id": {"get_param": "external_network_id"}, "port_id": {"get_attr": ["pool", "vip", "port_id"]}}}, "pool": {"type": "OS::Neutron::Pool", "properties": {"subnet_id": {"get_param": "subnet_id"}, "vip": {"protocol_port": 80}, "lb_method": "LEAST_CONNECTIONS", "protocol": "HTTP", "monitors": [{"get_resource": "monitor"}]}}, "web_server_scaledown_policy": {"type": "OS::Heat::ScalingPolicy", "properties": {"auto_scaling_group_id": {"get_resource": "asg"}, "adjustment_type": "change_in_capacity", "scaling_adjustment": -1, "cooldown": 30}}}}})
        c = pycurl.Curl()   #Open CURL
        c.setopt(c.URL, str(heat_endpoint+"/stacks"))    #Define Heat endpoint
        c.setopt(c.HTTPHEADER, ['User-Agent: python-heatclient', 'Content-Type: application/json', str(tmp_token)])  #Create Type of parameter API
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        stack_return_str = buf.getvalue()
        buf.close()
        #print stack_return_str
        stack_return = json.loads(stack_return_str) #Convert srt to dir
        print timeclient.datetime.today(), "Create Stack:", stack_return["stack"]["id"] #Show after Create Stack
        return stack_return
    except:
        print timeclient.datetime.today(), "Error Can't Create Stack"  # Print after Create Stack
################# List Stack Orchestration Core by API #################
def list_stack_core():
    buf = cStringIO.StringIO()  # Create buffer string IO
    tmp_token = "X-Auth-Token: " + keystone.auth_token  # Define token for authen heat service
    c = pycurl.Curl()  # Open CURL
    c.setopt(c.URL, str(heat_endpoint + "/stacks"))  # Define Heat endpoint
    c.setopt(c.HTTPHEADER,
                ['User-Agent: python-heatclient', 'Content-Type: application/json',
                str(tmp_token)])  # Create Type of parameter API
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.perform()
    stack_list_return_str = buf.getvalue()
    buf.close()
    stack_list_return = json.loads(stack_list_return_str)  # Convert srt to dir
    return stack_list_return
################# List Stack Orchestration #################
def list_stack():
    try:
        list_stack_return = list_stack_core()
        tmp_list_stacl_return = list()
        for tmp_list_stack in list_stack_return["stacks"]:
            tmp_list_stacl_return.append(str(tmp_list_stack["id"]))
        if tmp_list_stacl_return == list():  # If not list value
            tmp_list_stacl_return.append("Empty")  # Insert Empty to print
        print timeclient.datetime.today(), "List all Stack:", tmp_list_stacl_return  # Print after List all Stack
        return list_stack_return
    except:
        print timeclient.datetime.today(), "Error Can't List all Stack"  # Print after List all Stack
################# Delete Stack Orchestration by API #################
def delete_stack(stack_name=str(), stack_id=str()):
    try:
        buf = cStringIO.StringIO()  # Create buffer string IO
        tmp_token = "X-Auth-Token: " + keystone.auth_token  # Define token for authen heat service
        c = pycurl.Curl()  # Open CURL
        c.setopt(c.URL, str(heat_endpoint+"/stacks/"+stack_name+"/"+stack_id))  # Define Heat endpoint
        c.setopt(c.HTTPHEADER,
                    ['User-Agent: python-heatclient', 'Content-Type: application/json',
                    str(tmp_token)])  # Create Type of parameter API
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        c.perform()
        stack_list_return_str = buf.getvalue()
        buf.close()
        print timeclient.datetime.today(), "Delete Stack:", stack_name, stack_id  # Print after delete Alarm
        return {"stack_name": stack_name, "id": stack_id}
    except:
        print timeclient.datetime.today(), "Error Can't Delete Stack ID:", stack_name, stack_id  # Print after delete Stack
################# Sleep time for create Stack #################
def sleep_status_stack(id_stack=str(), time_out=int()):
    try:
        tmp_status = True  # Status for exit loop
        tmp_find_vm = str()  # Find Stack
        tmp_count_time = 0  # count time
        while (tmp_status):  # Run any time
            tmp_list_stack_return = list_stack_core()  # List all Stack
            for tmp_server in tmp_list_stack_return["stacks"]:  # Select 1 of all Stack
                if tmp_server["id"] == id_stack:  # Select vm same name parameter
                    tmp_find_vm = tmp_server["stack_name"]
                    if tmp_server["stack_status"] == "CREATE_IN_PROGRESS":  # If status build sleep 1s
                        sleep.sleep(1)  # sleep 1s
                        tmp_count_time = tmp_count_time + 1  # count time 1s
                    elif tmp_server["stack_status"] == "CREATE_COMPLETE":  # If status active for exit
                        tmp_status = False  # Exit
                        print timeclient.datetime.today(), "Status Stack Complete:", tmp_server["id"], tmp_server["stack_status"], "in", tmp_count_time, "sec."  #
            if len(tmp_list_stack_return["stacks"]) == 0 or tmp_find_vm == str():
                tmp_status = False  # Exit
                print timeclient.datetime.today(), "Don't have Stack:", id_stack
            elif tmp_count_time == time_out:
                tmp_status = False  # Exit
                print timeclient.datetime.today(), "Time out Stack:", id_stack, "in", time_out, "sec."
    except:
        print timeclient.datetime.today(), "Error Can't Sleep Status Stack"

################# Create Auto Scaling Standard #################
def create_auto_standard(typescaling=1,vmmax=3,vmmin=1):
################# Initial #################
    tmp_token=str(uuid.uuid4())
################# 1 Create Pool #################
    show_subnet_private_return=find_subnet_id(name="private") #find subnet id for create lb
    create_pool_return=create_pool(subnet_id=show_subnet_private_return,name="pool-"+tmp_token)  #create lb in put subnet id
################# 2 Create vip #################
    vip_pool_return=create_vip(name_vip_pool="vip-"+tmp_token, subnet_id=show_subnet_private_return, pool_id=create_pool_return.get('pool')['id'])   #create vip lb and add to lb input lb id
################# 3 Create Floating #################
    find_network_return=find_network_id(name="public")  #find network id
    create_float_return=create_floating(floating_network_id=find_network_return) #create floating ip for vip
################# 4 Associate Floating #################
    associate_floating_return=associate_floating(port_id=vip_pool_return.get('vip')['port_id'],floating_id=create_float_return.get('floatingip')['id'])    #associate floating to vip input floating id and vip id
################# 5 Create Health Monitor #################
    create_health_monitor_return=create_health_monitor() #create health monitor for vip lb
################# 6 Associate Health Monitor #################
    associate_health_monitor_return=associate_health_monitor(pool=create_pool_return.get('pool')['id'],health_monitor=create_health_monitor_return.get('health_monitor')['id'])    #associate health monitor to vip input lb id and health monitor id
################# 7 Create High CPU #################
    action_url_high_cpu="http://"+str(show_command_server_ip(detail="Action High"))+":8888/high-cpu"   #create part for receive action cpu high
    action_url_high_cpu_return = create_alarm(alarm_actions=action_url_high_cpu,threshold=70,value=tmp_token,comparison_operator="gt",repeat_actions=True,name="cpu-high-"+tmp_token,evaluation_periods=1,period=30)  #create alarm cpu high input part and cpu>70
################# 8 Create Low CPU #################
    action_url_low_cpu="http://"+str(show_command_server_ip(detail="Action Low"))+":8888/low-cpu"    #create part for receive action cpu low
    action_url_low_cpu_return = create_alarm(alarm_actions=action_url_low_cpu,threshold=15,value=tmp_token,comparison_operator="lt",repeat_actions=True,name="cpu-low-"+tmp_token,evaluation_periods=1,period=30)   #create alarm cpu low input part and cpu<15
################# Receive Action and Action for Auto Scaling #################
    receive_alarm_return = str()  #Receive Action Value
    while(True):
        tmp_list_vm_return=list_vm()
################# 9 Create VM #################
        if ((tmp_list_vm_return==list() or receive_alarm_return=="high-cpu") and len(tmp_list_vm_return)<vmmax):  #scal out if tmp_list_vm_return empty or cpu higth and vm not over 3
            tmp_name_vm="vm-"+tmp_token+"-"+str(len(tmp_list_vm_return))
            if typescaling== 1:
                float_size = "m1.tiny.s"
                weight_member = 1
            elif typescaling== 2:
                if((len(tmp_list_vm_return)%3)==0): ##select small
                    float_size="m1.tiny.s"
                    weight_member=1
                elif ((len(tmp_list_vm_return) % 3) == 1): ##select medium
                    float_size = "m1.tiny.m"
                    weight_member=2
                elif ((len(tmp_list_vm_return) % 3) == 2): ##select large
                    float_size = "m1.tiny.l"
                    weight_member=4
            create_vm_return = create_vm(image_name="corec",flavors_name=float_size,meta_name=tmp_token,vm_name=tmp_name_vm)  #create new vm
            sleep_status_vm(name=tmp_name_vm, time_out=90) #wight time for create vm
################# 10 Create Member #################
            show_ip_create_return = show_ip_vm(create_vm_return)    #get ip from vm
            create_member_return = create_member(weight=weight_member,address=show_ip_create_return,pool_id=create_pool_return.get('pool')['id'])  #create member for lb by ip vm
            print timeclient.datetime.today(), "Scale Out Action Maximum ", vmmax, " VM, Now VM:", len(tmp_list_vm_return)
################# 13 Delete Member #################
        elif (receive_alarm_return=="low-cpu" and len(tmp_list_vm_return)>vmmin):   #scal in
################# Find Maximum VM for Delete #################
            tmp_list_member_return=list_member()
            show_ip_delete_return=str()
            tmp_max = 0  # first initialize min
            tmp_max_vm_name = str()  # first name
            for tmp_server in tmp_list_vm_return:  # find name min vm for delete
                if tmp_max < int(tmp_server.name[40:]):  # find min server name
                    tmp_max_vm_name = tmp_server.name  # save name to tmp name
                    show_ip_delete_return = show_ip_vm(tmp_max_vm_name)  #get ip from vm
                    tmp_max = int(tmp_server.name[40:]) #change max
##############################################################
            for tmp_delete_member in tmp_list_member_return["members"]:    #find member
                if tmp_delete_member["address"] == show_ip_delete_return:    #find ip same member list
                    delete_member_return = delete_member(member=tmp_delete_member["id"])    #remove vm form member
################# 12 Delete VM #################
            delete_vm_return = delete_vm(tmp_max_vm_name)  #delete vm by min name vm
            print timeclient.datetime.today(), "Scale In Action Minimum ", vmmin, " VM, Now VM:", len(tmp_list_vm_return)
################# Not Scale In #################
        elif (receive_alarm_return=="high-cpu" and len(tmp_list_vm_return) == vmmax):  # not scal out
            print timeclient.datetime.today(), "Can't Scale Out Action Maximum ",vmmax , " VM, Now VM:", len(tmp_list_vm_return)
################# Not Scale In #################
        elif (receive_alarm_return == "low-cpu" and len(tmp_list_vm_return) == vmmin):  # not scal in
            print timeclient.datetime.today(), "Can't Scale In Action Minimum ",vmmin , " VM, Now VM:", len(tmp_list_vm_return)
################# Not Responding #################
        else:
            print timeclient.datetime.today(), "Can't Responding for This Action:", receive_alarm_return
################# 11 Receive Alarm #################
        receive_alarm_return = open_receive_alarm()  #open socket for receive alarm

################# Remove All Config #################
def remove_all_config():
################# 1 Delete All VM #################
    #try:
    list_vm_return = list_vm()  #lisr all vm
    for tmp_vm_list in list_vm_return:
        delete_vm_return = delete_vm(vm_name=tmp_vm_list.name)
    #except:
    #    print "Error delete vm"
################# 2 Delete All Alarm #################
    try:
        list_alarm_return=list_alarm()  #list all alarm config
        for tmp_alarm_list in list_alarm_return:    #loop for select id from list
            delete_alarm_return = delete_alarm(alarm_id=tmp_alarm_list.id)  #delete alarm from list by id
    except:
        print "Error delete all alarm"
################# 3 Delete Health Monitor #################
    try:
        list_health_return = list_health_monitors()   #list all health monitor
        for tmp_sing_health in list_health_return.get('health_monitors'):  #list single health monitor
            for tmp_pool in tmp_sing_health["pools"]:   #list pool associate by monotor
                dissociate_health_monitor_return = dissociate_health_monitor(pool=tmp_pool["pool_id"],health_monitor=tmp_sing_health["id"]) #disassociate by pood id and monitor id
            delete_health_monitor_return = delete_health_monitor(health_monitor=tmp_sing_health["id"]) #delete single health monitor
    except:
        print "Error delete health mornitor"
################# 4 Delete Floating IP #################
    try:
        list_floating_return = list_floating()   #list all floating ip
        for tmp_list_floating in list_floating_return.get('floatingips'):   #list single floating ip
            delete_floatingip_return=delete_floating(floatingip=tmp_list_floating["id"]) #delete single floating ip
    except:
        print "Error delete floating ip"
################# 5 Delete VIP #################
    try:
        list_vip_return=list_vip()  #list all vip
        for tmp_vip in list_vip_return.get('vips'): #list single vip
            delete_vip_return=delete_vip(vip=tmp_vip["id"]) #delete single vip
    except:
        print "Error delete vip"
################# 6 Delete Pool #################
    try:
        list_pool_return = list_pool()  #list all pool
        for tmp_list_pool in list_pool_return.get('pools'): #list single pool
            delete_pool_return=delete_pool(id_pool=tmp_list_pool["id"]) #delete single pool
    except:
        print "Error delete pool"

################# Create Auto Scaling HOT #################
def create_hot():
    create_stack_return=create_stack() #Create stack
    sleep_status_stack(id_stack=create_stack_return["stack"]["id"],time_out=120)    #sleep for stack create complete

################# Remove HOT Config #################
def remove_hot_config():
    list_stack_return = list_stack()  # lisr all stack
    for tmp_stack_list in list_stack_return["stacks"]:
        delete_stack_return = delete_stack(stack_name=tmp_stack_list["stack_name"] ,stack_id=tmp_stack_list["id"])  #delete stack

################# RUN Main #################
print "[1] Create Auto Scaling SDK\n[2] Remove all Configuration SDK\n[3] Create Auto Scaling HOT\n" \
"[4] Remove all Configuration HOT\n[5] Debug Function\n[x] Exit"
tmp_input1 = input("Enter number: ")
if tmp_input1 == 1:
    #create_auto_standard() #Create stack by SDK STD
    print "[1] Auto Scaling Same Size\n[2] Auto Scaling Difference Size"
    tmp_input2 = input("Enter number: ")
    if tmp_input2 == 1:
        print "Auto Scaling Same Size"
        tmp_input3 = input("Enter number of maximum: ")
        tmp_input4 = input("Enter number of minimum: ")
        create_auto_standard(typescaling=1,vmmax=tmp_input3,vmmin=tmp_input4)  # Create Auto Scaling Same Size
    elif tmp_input2 == 2:
        print "Auto Scaling Difference Size"
        tmp_input3 = input("Enter number of maximum vm: ")
        tmp_input4 = input("Enter number of minimum vm: ")
        create_auto_standard(typescaling=2,vmmax=tmp_input3,vmmin=tmp_input4)  # Auto Scaling Difference Size
elif tmp_input1 == 2:
    remove_all_config()  # Remove all config
elif tmp_input1 == 3:
    create_hot()  # Create stack by HOT
elif tmp_input1 == 4:
    remove_hot_config() # Remove all HOT config
elif tmp_input1 == 5:
    print "Don't have any function!"
else:
    print "Bye Bye!"