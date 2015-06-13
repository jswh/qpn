#!/bin/python
import qingcloud.iaas
import time, os, sys
import json
class Vpn(object) :
    configFile = "config.json"
    routerId = ''
    vpnSetting = None
    hostName = ''
    conn = None

    def __init__(self, vpn = 'default') :
        if not os.path.exists(sys.path[0] + '/' + self.configFile) :
            print 'config file is not exits'
            sys.exit()
        else :
            f = file(self.configFile)
            conf = json.load(f)
            f.close()
            self.vpnSetting = conf['vpn_settings'].get(vpn);
            if not self.vpnSetting :
                print 'no vpn config named ' + vpn
                sys.exit()
            self.hostName = conf['host_name']
            self.routerId = conf['router_id']
            self.conn = qingcloud.iaas.connect_to_zone('AP1', conf['key_id'].encode('ascii'), conf['key'].encode('ascii'))

#router info check functions
    def getRouterInfo(self) :

        return self.conn.describe_routers([self.routerId])['router_set'][0]

    def getRouterEipInfo(self) :

        return self.getRouterInfo()['eip']

    def checkRouterStatus(self, status) :

        return self.getRouterInfo()['status'] == status
    
    def isRouterActive(self) :
        
        return self.checkRouterStatus('active')

    def isRouterPoweroff(self) :

        return self.checkRouterStatus('poweroffed')

    def isRouterUpdating(self) :

        return self.getRouterInfo()['transition_status'] == 'updating'
#router operation
    def poweronRouter(self) :
        self.conn.poweron_routers([self.routerId])

    def poweroffRouter(self) :
        self.conn.poweroff_routers([self.routerId])
    
    def bindEipToRouter(self, eip) :
        self.conn.modify_router_attributes(router = self.routerId, eip = eip)
        self.conn.update_routers([self.routerId])
#eip operation
    def allocateEip(self) :
        ret = self.conn.allocate_eips(bandwidth = self.vpnSetting['bandwidth'], billing_mode=self.vpnSetting['billing_mode'])

        return ret['eips'][0]
    def releaseEips(self) :
        eip = self.getRouterEipInfo()['eip_id']
        if eip :
            self.conn.release_eips([eip])
#change host
    def changeHosts(self) :
        with open('/etc/hosts', 'rt') as f:
            s = f.read().split('\n')
            with open('/tmp/etc_hosts.tmp', 'wt') as outf:
                for line in s :
                    if line.find(self.hostName) == -1 :
                        outf.write(line + '\n')
                outf.write(self.getRouterEipInfo()['eip_addr'] + '\t' + self.hostName)
                os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

    #vpn operation
    def vpnon(self) :
        if not self.isRouterActive() :
            self.poweronRouter() 

        eip = self.allocateEip()

        while True :
            if self.isRouterActive() :
                break
            else :
                print "routering is not active yet, wait another 5s"
                time.sleep(5)

        self.bindEipToRouter(eip)

        while True :
            if self.isRouterUpdating() :
                break
            else :
                print "routering is updating yet, wait another 5s"
                time.sleep(5)
        print 'pptp vpn ip address is ' + self.getRouterEipInfo()['eip_addr']
        print "set ip to host name :" + self.hostName
        self.changeHosts()
        print "done"

    def vpnoff(self):
        self.poweroffRouter()
        while True :
            if self.isRouterPoweroff() :
                break;
            else :
                print "router is not poweroffed yet, wait another 5s"
                time.sleep(5)
        print "release ip"
        self.releaseEips()
        print 'done'
