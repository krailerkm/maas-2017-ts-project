## MAAS v2017
**PROPOSED APPROACH**
The MASS software has been developed using Python 2.7 and OpenStack Mitaka. This software is an independent software that interface with OpenStack using OpenStack REST API. MASS communicate with Ceilometer to get the workload information. 

![](images/f1_pic.jpg)
Figure 1. The interaction between MASS software and OpenStack components

As MASS start, a pool of resources will be created in OpenStack using API, then a set point of maximum workload and minimum workload will be set into Ceilometer. When the workload increases and exceeds the maximum set point, Ceilometer will report back as a notification to MASS. Upon receiving the notification, MASS will execute the workload scaling policy, then use OpenStack API to create a new VM to enable a workload sharing on more physical machines.  If the workload decreases and becomes less than the minimum threshold, the notification will be sent to MASS. Upon receiving the notification, MASS will make a decision based on its policy and shutdown some VM to save the resources. The policy can be easily coded into the MASS system. Currently, the policy available is only the round-robin VM creation on the physical machine. 

**CONCEPT & ENVIRONMENT LAB**
The test environment composed of a set of 7 computers.  One computer is used as an OpenStack controller and 2 more are used as OpenStack compute nodes base on CPU Intel Q6600 2.4Ghz, Memory 6GB DDR2, HDD80GB SATA.  The rest are used as load generator. The test has been conducted using Jmeter version 3.1 (B. Erinle, 2014) as the workload generator. The main load test computer base on CPU Intel I7-4700MQ 2.4Ghz, Memory 16GB DDR3, SSD240GB SATA installed with Windows 7 and two more load test slave base on CPU Intel E750 2.93Ghz, Memory 2GB DDR3, HDD160GB SATA for Jmeter used CentOS7.  The rest is installed with Linux CentOS Version 7.2. The test configuration is as shown in Figure. 2. In this test, we pre-created 3 VM types; small size (s), medium size (M), and large size (L). 

![](images/f2_pic.jpg)
Figure 2. The test system configuration

Keyword : OpenStack, Cloud Computing, Cloud Media Server, Auto-Scaling Software

This software was part of Teshis when I was at university. Thank you to all who are interested.

## Installation
Pre-Software Request for MAAS Controller

```
CentOS 7.2
Python 2.7
OpenStack Client & Software Development Kit
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Unlicense](https://unlicense.org)
