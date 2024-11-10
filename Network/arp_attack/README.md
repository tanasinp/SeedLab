# ARP Cache Poisoning Attack Lab

For `Mac` with an Apple M-series chip

**VMware Fusion:** [VMware Fusion 13 Pro 13.5.2](https://customerconnect.vmware.com/en/evalcenter?p=fusion-player-personal-13) or [From my drive](https://drive.google.com/file/d/1r93EjCoikbehD6aaPDMhJCsoqPh11t2t/view?usp=sharing)

**VM version:** [SEED Ubuntu-20.04 VM](https://seedsecuritylabs.org/labsetup.html) or [From my drive](https://drive.google.com/file/d/1IPzOHrPnvwh5saghyQwFgCjSAsM2ZfZZ/view?usp=drive_link)

# Tasks 

**Network Setup:**

Host A: IP address `10.9.0.5`

Host B: IP address `10.9.0.6`

Host M (Attacker): IP address `10.9.0.105`

```
seed@seed-virtual-machine:~/Downloads/ARP_Labsetup-arm$ dockps
136d1a8eebf6  A-10.9.0.5
ecd9e3d4e6d9  B-10.9.0.6
6b08c9a19e82  M-10.9.0.105
```

Host A: MAC address ``02:42:0a:09:00:05``

Host B: MAC address ``02:42:0a:09:00:06``

Host M (Attacker): MAC address ``02:42:0a:09:00:69``

```
root@136d1a8eebf6:/# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.9.0.5  netmask 255.255.255.0  broadcast 10.9.0.255
        ether 02:42:0a:09:00:05  txqueuelen 0  (Ethernet)
        RX packets 2365  bytes 135359 (135.3 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2321  bytes 120678 (120.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

This is MAC address of host A: ether ``02:42:0a:09:00:05``


## Task 1 

### Task 1.A

The goal is to poison Host A’s ARP cache by sending an ARP request that associates Host B’s IP address with Host M’s MAC address.

Running the Python Script: ``1A_arp_poisoning.py`` .

Check ARP Cache on Host A:

```
root@136d1a8eebf6:/# arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.9.0.6                 ether   02:42:0a:09:00:69   C                     eth0
```

The ARP cache on Host A now maps Host B’s IP address to Host M’s MAC address after running the attack.

### Task 1.B

The goal is to poison Host A’s ARP cache by sending an ARP reply that associates Host B’s IP address with Host M’s MAC address.

Running the Python Script: ``1B_arp_poisoning.py`` .

Check ARP Cache on Host A:

```
root@136d1a8eebf6:/# arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.9.0.6                 ether   02:42:0a:09:00:70   C                     eth0
```

Scenario 1: B's IP address is already in A's cache.
- A's ARP table changes B's IP to the spoofed MAC address.

Scenario 2: B's IP address is not in A's cache.
- A's ARP table doesn't change.

### Task 1.C

The goal is to use a Gratuitous ARP to update Host A’s ARP cache, mapping Host B’s IP address to Host M’s MAC address.

Running the Python Script: ``1C_arp_poisoning.py`` .

Check ARP Cache on Host A:

```
root@136d1a8eebf6:/# arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.9.0.6                 ether   02:42:0a:09:00:69   C                     eth0
```
ARP gratuitous packet is a special ARP request packet. It is used when a host machine needs to
update outdated information on all the other machine's ARP cache. The gratuitous ARP packet has
the following characteristics:

- The source and destination IP addresses are the same, and they are the IP address of the host
issuing the gratuitous ARP.

- The destination MAC addresses in both ARP header and Ethernet header are the broadcast MAC
address (ff:ff:ff:ff:ff:ff).

## Task 2

The goal is to poison the ARP cache and intercept communication between Host A and Host B using ``Telnet``.


Before starting the communication on Host A and Host B, run the ``spoofMiTM.py`` script on Host M:

```
root@6b08c9a19e82:/volumes# python3 netcatSpoof.py
```

On Host A, initiate a Telnet connection to Host B:
```
root@136d1a8eebf6:/# telnet 10.9.0.6
```

Host M acts as the attacker, intercepting and modifying traffic between Host A and Host B. Running the Python Script: ``telnetSpoof.py`` .
```
root@6b08c9a19e82:/volumes# python3 telnetSpoof.py
```

**Observation:** 
```
root@6b08c9a19e82:/# sysctl net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
root@6b08c9a19e82:/# sysctl net.ipv4.ip_forward=0
net.ipv4.ip_forward = 0
```
- With IP Forwarding = 1:
  
  Host M allows it to act as a router by forwarding traffic between Host A and Host B. 

- With IP Forwarding = 0:

  Host M will intercept the Netcat traffic, the connection will drop.

## Task 3

The goal is to intercept and modify the communication between Host A and Host B using ``Netcat`` after successfully poisoning the ARP cache.

Before starting the communication on Host A and Host B, run the ``spoofMiTM.py`` script on Host M:

```
root@6b08c9a19e82:/volumes# python3 spoofMiTM.py
```

Host B acts as a Netcat server, listening on port 9090, while Host A connects to it.

On Host B, run the Netcat listener:
```
root@ecd9e3d4e6d9:/# nc -lp 9090
```

On Host A, connect to Host B using Netcat:
```
root@136d1a8eebf6:/# nc 10.9.0.6 9090
```

Host M acts as the attacker, intercepting and modifying traffic between Host A and Host B. Running the Python Script: ``netcatSpoof.py`` .

```
root@6b08c9a19e82:/volumes# python3 netcatSpoof.py
```

**Observation:** 
```
root@6b08c9a19e82:/# sysctl net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
root@6b08c9a19e82:/# sysctl net.ipv4.ip_forward=0
net.ipv4.ip_forward = 0
```
- With IP Forwarding = 1:
  
  Host M allows it to act as a router by forwarding traffic between Host A and Host B. 

- With IP Forwarding = 0:

  Host M will intercept the Netcat traffic, the connection will drop.

