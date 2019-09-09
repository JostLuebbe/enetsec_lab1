from scapy.all import *

packet = IP(dst='127.0.0.1', id=1111, ttl=99)/TCP(srcport=RandShort(), dstport=12000, seq=12345, ack=100)

i=1

while 1:
    send(packet, inter=.001)
    print(f'packet sent:  {i}')
    i += 1


# ls(packet)
#
# ans, unans = srloop(packet, inter=0.3, retry=2, timeout=4)
#
# ans.summary()
#
# unans.summary()

# rsv = sr(packet)

# print(packet.show())