from scapy.all import IP, TCP, sr

packet = IP(dst='127.0.0.1', src='8.8.8.8')/TCP(dport=12000)

rsv = sr(packet)

# print(packet.show())