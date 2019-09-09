from scapy.all import IP, TCP, sr

packet = IP(dst='127.0.0.1', src='8.8.8.8', id=1111, ttl=99)/TCP(sport=RandShort(), dport=12000, seq=12345, ack=100)
ls(packet)

ans, unans = srloop(packet, inter=0.3, retry=2, timeout=4)

ans.summary()

unans.summary()

rsv = sr(packet)

# print(packet.show())