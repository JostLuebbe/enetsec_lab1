from scapy.all import *

conf.iface="lo0"
conf.L3socket = L3RawSocket

packet = IP(dst='127.0.0.2', id=1111, ttl=99)/TCP(sport=RandShort(), dport=12000, flags='S')


# i = 1
#
# while 1:
#     rsv = sr(packet, inter=.001)
#     print('packet sent: ', i)
#     i += 1


ls(packet)

ans, unans = srloop(packet, inter=0.3, retry=2, timeout=4)

ans.summary()

unans.summary()

# rsv = sr(packet)

# print(packet.show())