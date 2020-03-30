#!/bin/bash
id_pools=8d212118-5b02-4a9c-9aea-79677c7ce4cd
id_vm1=a368dfd4-f61b-47ef-b0c5-207315ed8537
id_vm2=1de53a6c-dfc1-4657-9da7-47cd3ccfcf4e
id_vm1_net=instance-0000016a-a368dfd4-f61b-47ef-b0c5-207315ed8537-tapc4e2362c-12
id_vm2_net=instance-0000016b-1de53a6c-dfc1-4657-9da7-47cd3ccfcf4e-tap22523409-18

mkdir -p output_log
pwd
cd output_log
pwd

#POOL cpu_util
ceilometer sample-list -m cpu_util -q metadata.user_metadata.stack=$id_pools >> sample-list-mcpu_util.txt
ceilometer statistics -m cpu_util -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mcpu_util.txt
#VM1
ceilometer sample-list -m cpu_util -q resource_id=$id_vm1 >> sample-list-mcpu_util_vm1.txt
ceilometer statistics -m cpu_util -q resource_id=$id_vm1 -p 30 -a avg >> statistics-mcpu_util_vm1.txt
#VM2
ceilometer sample-list -m cpu_util -q resource_id=$id_vm2 >> sample-list-mcpu_util_vm2.txt
ceilometer statistics -m cpu_util -q resource_id=$id_vm2 -p 30 -a avg >> statistics-mcpu_util_vm2.txt

#POOL memory.usage
ceilometer sample-list -m memory.usage -q metadata.user_metadata.stack=$id_pools >> sample-list-mmemory.usage.txt
ceilometer statistics -m memory.usage -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mmemory.usage.txt
#VM1
ceilometer sample-list -m memory.usage -q resource_id=$id_vm1 >> sample-list-mmemory.usage_vm1.txt
ceilometer statistics -m memory.usage -q resource_id=$id_vm1 -p 30 -a avg >> statistics-mmemory.usage_vm1.txt
#VM2
ceilometer sample-list -m memory.usage -q resource_id=$id_vm2 >> sample-list-mmemory.usage_vm2.txt
ceilometer statistics -m memory.usage -q resource_id=$id_vm2 -p 30 -a avg >> statistics-mmemory.usage_vm2.txt

#POOL disk.read.requests.rate
ceilometer sample-list -m disk.read.requests.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mdisk.read.requests.rate.txt
ceilometer statistics -m disk.read.requests.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mdisk.read.requests.rate.txt
#VM1
ceilometer sample-list -m disk.read.requests.rate -q resource_id=$id_vm1 >> sample-list-mdisk.read.requests.rate_vm1.txt
ceilometer statistics -m disk.read.requests.rate -q resource_id=$id_vm1 -p 30 -a avg >> statistics-mdisk.read.requests.rate_vm1.txt
#VM2
ceilometer sample-list -m disk.read.requests.rate -q resource_id=$id_vm2 >> sample-list-mdisk.read.requests.rate_vm2.txt
ceilometer statistics -m disk.read.requests.rate -q resource_id=$id_vm2 -p 30 -a avg >> statistics-mdisk.read.requests.rate_vm2.txt

#POOL disk.write.requests.rate
ceilometer sample-list -m disk.write.requests.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mdisk.write.requests.rate.txt
ceilometer statistics -m disk.write.requests.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mdisk.write.requests.rate.txt
#VM1
ceilometer sample-list -m disk.write.requests.rate -q resource_id=$id_vm1 >> sample-list-mdisk.write.requests.rate_vm1.txt
ceilometer statistics -m disk.write.requests.rate -q resource_id=$id_vm1 -p 30 -a avg >> statistics-mdisk.write.requests.rate_vm1.txt
#VM2
ceilometer sample-list -m disk.write.requests.rate -q resource_id=$id_vm2 >> sample-list-mdisk.write.requests.rate_vm2.txt
ceilometer statistics -m disk.write.requests.rate -q resource_id=$id_vm2 -p 30 -a avg >> statistics-mdisk.write.requests.rate_vm2.txt

#POOL disk.read.bytes.rate
ceilometer sample-list -m disk.read.bytes.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mdisk.read.bytes.rate.txt
ceilometer statistics -m disk.read.bytes.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mdisk.read.bytes.rate.txt
#VM1
ceilometer sample-list -m disk.read.bytes.rate -q resource_id=$id_vm1 >> sample-list-mdisk.read.bytes.rate_vm1.txt
ceilometer statistics -m disk.read.bytes.rate -q resource_id=$id_vm1 -p 30 -a avg >> statistics-mdisk.read.bytes.rate_vm1.txt
#VM2
ceilometer sample-list -m disk.read.bytes.rate -q resource_id=$id_vm2 >> sample-list-mdisk.read.bytes.rate_vm2.txt
ceilometer statistics -m disk.read.bytes.rate -q resource_id=$id_vm2 -p 30 -a avg >> statistics-mdisk.read.bytes.rate_vm2.txt

#POOL disk.write.bytes.rate
ceilometer sample-list -m disk.write.bytes.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mdisk.write.bytes.rate.txt
ceilometer statistics -m disk.write.bytes.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mdisk.write.bytes.rate.txt
#VM1
ceilometer sample-list -m disk.write.bytes.rate -q resource_id=$id_vm1 >> sample-list-mdisk.write.bytes.rate_vm1.txt
ceilometer statistics -m disk.write.bytes.rate -q resource_id=$id_vm1 -p 30 -a avg >> statistics-mdisk.write.bytes.rate_vm1.txt
#VM2
ceilometer sample-list -m disk.write.bytes.rate -q resource_id=$id_vm2 >> sample-list-mdisk.write.bytes.rate_vm2.txt
ceilometer statistics -m disk.write.bytes.rate -q resource_id=$id_vm2 -p 30 -a avg >> statistics-mdisk.write.bytes.rate_vm2.txt

#POOL network.incoming.bytes.rate
ceilometer sample-list -m network.incoming.bytes.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mnetwork.incoming.bytes.rate.txt
ceilometer statistics -m network.incoming.bytes.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mnetwork.incoming.bytes.rate.txt
#VM1
ceilometer sample-list -m network.incoming.bytes.rate -q resource_id=$id_vm1_net >> sample-list-mnetwork.incoming.bytes.rate_vm1.txt
ceilometer statistics -m network.incoming.bytes.rate -q resource_id=$id_vm1_net  -p 30 -a avg >> statistics-mnetwork.incoming.bytes.rate_vm1.txt
#VM2
ceilometer sample-list -m network.incoming.bytes.rate -q resource_id=$id_vm2_net >> sample-list-mnetwork.incoming.bytes.rate_vm2.txt
ceilometer statistics -m network.incoming.bytes.rate -q resource_id=$id_vm2_net  -p 30 -a avg >> statistics-mnetwork.incoming.bytes.rate_vm2.txt

#POOL network.outgoing.bytes.rate
ceilometer sample-list -m network.outgoing.bytes.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mnetwork.outgoing.bytes.rate.txt
ceilometer statistics -m network.outgoing.bytes.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mnetwork.outgoing.bytes.rate.txt
#VM1
ceilometer sample-list -m network.outgoing.bytes.rate -q resource_id=$id_vm1_net >> sample-list-mnetwork.outgoing.bytes.rate_vm1.txt
ceilometer statistics -m network.outgoing.bytes.rate -q resource_id=$id_vm1_net  -p 30 -a avg >> statistics-mnetwork.outgoing.bytes.rate_vm1.txt
#VM2
ceilometer sample-list -m network.outgoing.bytes.rate -q resource_id=$id_vm2_net  >> sample-list-mnetwork.outgoing.bytes.rate_vm2.txt
ceilometer statistics -m network.outgoing.bytes.rate -q resource_id=$id_vm2_net  -p 30 -a avg >> statistics-mnetwork.outgoing.bytes.rate_vm2.txt

#POOL network.incoming.packets.rate
ceilometer sample-list -m network.incoming.packets.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mnetwork.incoming.packets.rate.txt
ceilometer statistics -m network.incoming.packets.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mnetwork.incoming.packets.rate.txt
#VM1
ceilometer sample-list -m network.incoming.packets.rate -q resource_id=$id_vm1_net  >> sample-list-mnetwork.incoming.packets.rate_vm1.txt
ceilometer statistics -m network.incoming.packets.rate -q resource_id=$id_vm1_net  -p 30 -a avg >> statistics-mnetwork.incoming.packets.rate_vm1.txt
#VM2
ceilometer sample-list -m network.incoming.packets.rate -q resource_id=$id_vm2_net  >> sample-list-mnetwork.incoming.packets.rate_vm2.txt
ceilometer statistics -m network.incoming.packets.rate -q resource_id=$id_vm2_net  -p 30 -a avg >> statistics-mnetwork.incoming.packets.rate_vm2.txt

#POOL network.outgoing.packets.rate
ceilometer sample-list -m network.outgoing.packets.rate -q metadata.user_metadata.stack=$id_pools >> sample-list-mcnetwork.outgoing.packets.rate.txt
ceilometer statistics -m network.outgoing.packets.rate -q metadata.user_metadata.stack=$id_pools -p 30 -a avg >> statistics-mnetwork.outgoing.packets.rate.txt
#VM1
ceilometer sample-list -m network.outgoing.packets.rate -q resource_id=$id_vm1_net >> sample-list-mnetwork.outgoing.packets.rate_vm1.txt
ceilometer statistics -m network.outgoing.packets.rate -q resource_id=$id_vm1_net -p 30 -a avg >> statistics-mnetwork.outgoing.packets.rate_vm1.txt
#VM2
ceilometer sample-list -m network.outgoing.packets.rate -q resource_id=$id_vm2_net >> sample-list-mnetwork.outgoing.packets.rate_vm2.txt
ceilometer statistics -m network.outgoing.packets.rate -q resource_id=$id_vm2_net -p 30 -a avg >> statistics-mnetwork.outgoing.packets.rate_vm2.txt

unset  id_pools
unset id_vm1
unset id_vm2
unset id_vm1_net
unset id_vm2_net
