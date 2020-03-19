from scapy.all import *


def main():
    syn = IP(dst='www.baiwanzhan.com') / TCP(dport=80, sport=22, flags='S')
    print(syn)
    syn_ack = sr1(syn)
    print(syn_ack)
    getStr = 'GET /www.baiwanzhan.com?query=%E7%BD%91%E7%90%83 HTTP/1.1 \n\n'
    request = IP(dst='www.baiwanzhan.com') / TCP(dport=80, sport=syn_ack[TCP].dport,
                                             seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
    reply = sr1(request)
    print(reply)


if __name__ == '__main__':
    main()