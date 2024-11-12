# Local DNS Attack Lab

For `Mac` with an Apple M-series chip

**VMware Fusion:** [VMware Fusion 13 Pro 13.5.2](https://customerconnect.vmware.com/en/evalcenter?p=fusion-player-personal-13) or [From my drive](https://drive.google.com/file/d/1r93EjCoikbehD6aaPDMhJCsoqPh11t2t/view?usp=sharing)

**VM version:** [SEED Ubuntu-20.04 VM](https://seedsecuritylabs.org/labsetup.html) or [From my drive](https://drive.google.com/file/d/1IPzOHrPnvwh5saghyQwFgCjSAsM2ZfZZ/view?usp=drive_link)

# Tasks 

## Tasks 1

In this task, our goal is to spoof the user machine’s DNS query. By running [`task_1_local_dns.py`](https://github.com/tanasinp/SeedLab/tree/main/Network/dns_local/files/task_1_local_dns.py) on the attacker host and executing `dig www.example.com` on the user host:

```
root@3dee8ea9c91f:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39211
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	259200	IN	A	10.0.2.5

;; Query time: 14 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 08:54:07 UTC 2024
;; MSG SIZE  rcvd: 64

root@3dee8ea9c91f:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8205
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	259200	IN	A	10.0.2.5

;; Query time: 13 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 08:54:08 UTC 2024
;; MSG SIZE  rcvd: 64

root@3dee8ea9c91f:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15559
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: ee4b2806c7b4f1df01000000673317b08d66456e1342b2e1 (good)
;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	3600	IN	A	93.184.215.14

;; Query time: 2 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 08:54:08 UTC 2024
;; MSG SIZE  rcvd: 88
```
The `www.example.com` resolves to `10.0.2.5` for about 2-3 times. This happens because the user machine initially sends a DNS query to the local DNS server, and while the local DNS server is still resolving the query, our spoofed response can intercept it. However, when the IP is cached in the local DNS server, subsequent queries will retrieve the cached IP instead of our spoofed one.

## Tasks 2

In this task, our goal is to spoof the Local DNS Server. By running [`task_2_local_dns.py`](https://github.com/tanasinp/SeedLab/tree/main/Network/dns_local/files/task_2_local_dns.py) on the attacker host and executing `dig www.example.com` on the user host: 

```
root@3dee8ea9c91f:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31741
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	259200	IN	A	10.0.2.5

;; Query time: 27 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 09:00:18 UTC 2024
;; MSG SIZE  rcvd: 64
```

This is in `Local DNS Server`'s cache:

```
example.com.		777546	NS	a.iana-servers.net.
			777546	NS	b.iana-servers.net.
; additional
			691146	DS	370 13 2 (
					BE74359954660069D5C63D200C39F5603827
					D7DD02B56F120EE9F3A86764247C )
; additional
			691146	RRSIG	DS 13 2 86400 (
					20241119012518 20241112001518 29942 com.
					xDTV+GSyIuGyeLLin8fd12iXoPr5EayvZ2L6
					xdC2YMjGKkxQksIS7e26iSR20EVYMPTmdA5I
					gdb0Eaf+XoA7Ng== )
; authanswer
www.example.com.	863947	A	10.0.2.5
```

We successfully manipulated the DNS response for `www.example.com` to return `10.0.2.5`. And the spoofed IP address(10.0.2.5) has now been stored in the Local DNS Server's cache.

## Tasks 3, 4

In these task, our goal is to spoof the Local DNS Server by inserting NS records (Authority Section) into the Local DNS Server's cache. By running [`task_3&4_local_dns.py`](https://github.com/tanasinp/SeedLab/tree/main/Network/dns_local/files/task_3&4_local_dns.py) on the attacker host and executing `dig www.example.com` on the user host: 

```
root@3dee8ea9c91f:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18279
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 1

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	259200	IN	A	10.0.2.5

;; AUTHORITY SECTION:
example.com.		259200	IN	NS	ns.attacker32.com.
google.com.		259200	IN	NS	ns.attacker32.com.

;; ADDITIONAL SECTION:
ns.attacker32.com.	259200	IN	A	10.9.0.153

;; Query time: 27 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 09:04:54 UTC 2024
;; MSG SIZE  rcvd: 180
```

This is in `Local DNS Server`'s cache:

```
; glue
example.com.		777546	NS	a.iana-servers.net.
			777546	NS	b.iana-servers.net.
; additional
			691146	DS	370 13 2 (
					BE74359954660069D5C63D200C39F5603827
					D7DD02B56F120EE9F3A86764247C )
; additional
			691146	RRSIG	DS 13 2 86400 (
					20241119012518 20241112001518 29942 com.
					xDTV+GSyIuGyeLLin8fd12iXoPr5EayvZ2L6
					xdC2YMjGKkxQksIS7e26iSR20EVYMPTmdA5I
					gdb0Eaf+XoA7Ng== )
; authanswer
www.example.com.	863947	A	10.0.2.5
```

The first record (`example.com`) is legitimate and will be in cache because `ns.attacker32.com` is set as the authoritative nameserver for `example.com`, but the second record (`google.com`) not in the cache because `ns.attacker32.com` is not responsible for google.com's zone. 

## Tasks 5

In these task, our goal is attemp injecting IP addresses into the Local DNS Server's cache via the Additional Section. By running [`task_5_local_dns.py`](https://github.com/tanasinp/SeedLab/tree/main/Network/dns_local/files/task_5_local_dns.py) on the attacker host and executing `dig www.example.com` on the user host:

```
root@3dee8ea9c91f:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25408
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 3

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	259200	IN	A	10.0.2.5

;; AUTHORITY SECTION:
example.com.		259200	IN	NS	ns.attacker32.com.
example.com.		259200	IN	NS	ns.example.com.

;; ADDITIONAL SECTION:
ns.attacker32.com.	259200	IN	A	1.2.3.4
ns.example.com.		259200	IN	A	5.6.7.8
www.facebook.com.	259200	IN	A	3.4.5.6

;; Query time: 21 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 09:11:55 UTC 2024
;; MSG SIZE  rcvd: 240

root@af9d4521243c:/# dig www.example.com

; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 16662
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 4f8690a3467e998c010000006733207ea34df8dcaa1ee033 (good)
;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	259198	IN	A	1.2.3.5

;; Query time: 2 msec
;; SERVER: 10.9.0.53#53(10.9.0.53)
;; WHEN: Tue Nov 12 09:31:42 UTC 2024
;; MSG SIZE  rcvd: 88

```

This is in `Local DNS Server`'s cache:

```
; answer
ns.attacker32.com.	615595	\-AAAA	;-$NXRRSET
; attacker32.com. SOA ns.attacker32.com. admin.attacker32.com. 2008111001 28800 7200 2419200 86400
; authanswer
			863995	A	10.9.0.153
; glue
example.com.		777595	NS	a.iana-servers.net.
			777595	NS	b.iana-servers.net.
; additional
			691195	DS	370 13 2 (
					BE74359954660069D5C63D200C39F5603827
					D7DD02B56F120EE9F3A86764247C )
; additional
			691195	RRSIG	DS 13 2 86400 (
					20241119012518 20241112001518 29942 com.
					xDTV+GSyIuGyeLLin8fd12iXoPr5EayvZ2L6
					xdC2YMjGKkxQksIS7e26iSR20EVYMPTmdA5I
					gdb0Eaf+XoA7Ng== )
; authanswer
_.example.com.		863995	A	10.0.2.5
; authanswer
ns.example.com.		863995	A	10.0.2.5
; authanswer
www.example.com.	863995	A	1.2.3.5
```

The `ns.example.com` and `ns.attacker32.com` are in to the cache but the `www.facebook.com` doesn't because it's not part of the same zone.

But when running `dig` command to find out `www.example.com`'s IP address, the server returns `1.2.3.5` instead of the cached `1.2.3.4` and `5.6.7.8` from the Additional Section. Because the `Local DNS Server` dosen't fully trust the IP address that in Additional record because they are “second-hand” information. The server prioritizes “first-hand” information from the Answer Section, leading it to perform a fresh query for verification.
 