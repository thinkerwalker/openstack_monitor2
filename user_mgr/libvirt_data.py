from __future__ import print_function
import sys
import libvirt
import time
from xml.etree import ElementTree
def getDomainMemUsed(domain):
    try:
        domain.setMemoryStatsPeriod(5)
        meminfo = domain.memoryStats()
        free_mem = float(meminfo['unused'])
        total_mem = float(meminfo['available'])
        util = ((total_mem-free_mem) / total_mem)*100
    except:
	#部分操作系统不支持某驱动
        try:
            actual = float(domain.memoryStats()['actual'])
            rss = float(domain.memoryStats()['rss'])
            rss = rss - 150000
            if rss >= actual:
                    rss = rss - 250000
            if rss <=0:
                    rss = rss + 150000
            #util = str(int((rss / actual)*100))
            util = (rss / actual)*100
            util = 'util:' + str(util) + '%'
            print (util)
        except:
            pass
    mem={"mem_free":free_mem,"mem_util":util}
    return mem
def getDomainCPUInfo(dom):
    #get time of cpu and real time
    ti = dict()
    ti['t'] = time.time()
    dominfo=dom.info()
    ti['ct'] = dominfo[4]
   # print('CPU:')
   # for a in dominfo:
    #    print(str(a),end=' ')
    #for k in ti:
    #    print(k)
    return ti

def getDomainCPUUsed(dom):
    tl=getDomainCPUInfo(dom)
    time.sleep(0.5)
    t=getDomainCPUInfo(dom)
    cpu_diff = (t['ct']-tl['ct'])/100000.0
    real_diff = 109.0*(t['t']-tl['t'])
    CPUUsed = 1.0*cpu_diff/real_diff
    cpu_info={"cpu_util":CPUUsed}
    return cpu_info

def getDomainNetork(dom):
    tree = ElementTree.fromstring(dom.XMLDesc())
    ifaces = tree.findall('devices/interface/target')
    #ifs = AD.interfaceStats('vnet0')
    for i in ifaces:
        iface = i.get('dev')
        tl = time.time()
        ifaceinfo = dom.interfaceStats(iface)
        rx_bl = ifaceinfo[0]
        tx_bl = ifaceinfo[4]
       # print(str(iface)+'ifo'+str(ifaceinfo))
        time.sleep(1)
        t=time.time()
        ifaceinfo = dom.interfaceStats(iface)
        rx_b = ifaceinfo[0]
        tx_b = ifaceinfo[4]
       # print(str(iface)+'ifo'+str(ifaceinfo))
        rx_v=(rx_b-rx_bl)/(t-tl)*1.0
        tx_v=(tx_b-tx_bl)/(t-tl)*1.0
        net_info={"up":tx_v,"down":rx_v,"received":ifaceinfo[0],"sent":ifaceinfo[4]}
        return net_info
        #print('     Down:'+str(round(rx_v,1))+'b/s    Up:'+str(round(tx_v,1))+'b/s')
        #print('     Total received: '+str(round((ifaceinfo[0]/1024.0),1))+'KiB   Total Sent: '+str(round((ifaceinfo[4]/1024.0),1))+'KiB')

def getDomainDisk(dom):
    tree = ElementTree.fromstring(dom.XMLDesc())
    devices = tree.findall('devices/disk/target')
    #ifs = AD.interfaceStats('vnet0')
    for d in devices:
        device = d.get('dev')
        tl = time.time()
        #devstat = dom.blockStats(device)
        devst = dom.blockStatsFlags(device,0)
        rd_bl = devst['rd_total_times']
        wr_bl = devst['wr_total_times']
        time.sleep(1)
        t=time.time()
        #devstat = dom.blockStats(device)
        devst = dom.blockStatsFlags(device,0)
        #for d in devstat:
         #   print(d)
        rd_b = devst['rd_total_times']
        wr_b = devst['wr_total_times']
        rd_v = (rd_b-rd_bl)/(t-tl)
        wr_v = (wr_b-wr_bl)/(t-tl)

        devinfo = dom.blockInfo(device,0)
        #for d in devinfo:
        #    print(d)
        disk_info={"read_v":round(rd_v,1),"write_v":round(wr_v,1),"total":round((devinfo[0]/1024.0)/1024.0/1024.0,1),"used":round(((devinfo[2]/1024.0)/1024.0)/1024.0,1)}
        #print('     Disk Read: '+str(round(rd_v,1))+'b/s    Write:'+str(round(wr_v,1))+'b/s')
        #print('     Disk Total: '+str(round((devinfo[0]/1024.0)/1024.0/1024.0,1))+'GB   Used: '+str(round(((devinfo[2]/1024.0)/1024.0)/1024.0,1))+'GB')
        return disk_info

def get_data(host,guest_name):
    conn=libvirt.open('qemu+tcp://%s/system'%(host))
    domain = conn.lookupByName(guest_name)
    mem_info=getDomainMemUsed(domain)
    cpu_info=getDomainCPUUsed(domain)
    net_info=getDomainNetork(domain)
    disk_info=getDomainDisk(domain)
    #print(disk_info)
    #print(net_info)
    #print(mem_info['mem_free'])
    #print(cpu_info['cpu_util'])
    libvirt_data={"mem_info":mem_info,"cpu_info":cpu_info,"net_info":net_info,"disk_info":disk_info}
    conn.close()   
    return libvirt_data
if __name__ == "__main__":
    get_data('192.168.10.23','instance-00000002')
