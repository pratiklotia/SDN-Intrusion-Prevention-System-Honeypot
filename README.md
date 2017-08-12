# SDN-Intrusion-Prevention-System-Honeypot

Intrusion Prevention System to dynamically add firewall rules to block malicious traffic detected by IDS system implemented on 
Software Defined Networl (SDN). Alternatively, the malicious traffic can be redirected to a Honeypot Server. 
OpenFlow protocol used for SDN. Snort used for IDS (Intrusion Detection System).

2 Files:
1. ips.py: IPS based on IDS Snort
2. ips_honey.py: Additional functionality to redirect malicious traffic to Honeypot Server.

![alt text](https://github.com/pratiklotia/SDN-Intrusion-Prevention-System-Honeypot/blob/master/topology-sdn_ips_honey.png)

•	Working of the project & implied Benefits:

	The project uses an Ubuntu v16.04 64-bit Operating System – VM.

	Floodlight, Mininet and Snort (along with dependencies) are installed and configured on the VM.

	For testing purposes, all rules of Snort except the local user rules have been disabled.

	Snort local rules file is configured with signatures of traffic like ICMP and HTTP.

	Floodlight controller is started and it runs on <localhost_IP> on port 8080.

	Mininet topology is initiated with 1 switch, 5 hosts having IP base of 10.0.0.0/24 with their respective X-terms and Open Virtual Switch interacting with Floodlight Controller using OpenFlow protocol version 1.3.

	The switch is set as a compatible OVS bridge.

	Port mirroring is enabled on OVS such as traffic generating from and directed to host 4 is mirrored on host 5’s network interface.

	For testing in real world environment, a hybrid router can be used in place of OVS and Router IP Traffic Export (RITE) can be enabled to mirror traffic.

	Due to mirroring, host 5 actually acts as a network sniffer.

	A security monitoring tool is started on host 5 to analyze all incoming traffic (both mirrored and non-mirrored). For this project, Snort tool has been used for testing. Alternatively tools for flow analysis like NetFlow & SiLK can be used too.

	For practical purposes, host 5 can be made inaccessible from the public environment so that only mirrored traffic is active on host 5 interface. This way there is no confusion about whether the traffic is for host 5 or for host 4. It will always be for host 4 – just mirrored on host 5.

	The alerts are directly logged into a text file.

	This Host can now act as an application layer for pushing flow entries to the switch via the Controller.

	A python script reads the alerts file and determines parameters such as source and destination IP, source and destination ports, protocols and Ethernet type, flags and other header values.

	The python script is configured to dynamically make flows entry matching fields using these parameters. These are written in JSON format. The flow entry supports all the theoretical variations supported by OpenFlow version 1.3 such as groups, buckets, timers, meter bands, modify fields, push & pop tags, timers, etc.

	The python script ensures to add a hard timeout value of a few seconds and a higher priority value in the flow entry. It is necessary to specify the switch DPID (data path identifier) and a unique name for the flow entry.

	Not specifying any action parameter will automatically notify the switch to drop any matching packet.

	This JSON format is properly encoded and sent as a POST message in a proper format using REST API directed to the controller IP and port which in turn pushes them to the OVS.

	In this way, suspicious traffic can be blocked on the Data Plane. This forms our IPS part.

	IDS can generate several false positives and this can lead to blocking of good traffic. Hence, a hard timeout of a few seconds is added so that the suspicious traffic is only temporarily blocked. This would considerably slow down attackers while only temporarily block good traffic.

	Alternatively we can have an additional functionality. Instead of blocking the traffic for a specific match field, it is possible to modify certain fields of the packet and alter its behavior. We can change the destination IP so that the traffic can be directed to a different system.

	Using this, we can redirect the traffic to a Honeypot system. The traffic can be analyzed here and we can understand the intent of the sender of the suspicious traffic. The honeypot system varies from application to application.

	Hence attacks can be mitigated using this method.

	This concludes the working of this project.



Tags:

SDN Security
Ryu, Floodlight
Data Plane
Attacker, victim, Mirror/RITE, load
IDS – Snort – alerts – log
IPS – using log file – params
Python – JSON
REST API – POST, DELETE
False Positives
+ Set Field
Honeypot – understand, intent, mitigate
Delete FP


For bugs, questions, request to use this project, etc. please email me at pratik.lotia@colorado.edu
