import socket
import zeroconf


def main():
    ip_addr = "127.0.0.1"
    coap_port = 15683
    instance = "usp-00D09E-RPi_Test-T0000000001"
    service = "_usp-agt-coap._udp."
    domain = "local."
    coap_url = "coap:\\\\" + ip_addr + ":" + str(coap_port) + "\\usp"

    svc_type = service + domain
    svc_name = instance + "." + service + domain
    svc_addr = socket.inet_aton(ip_addr)
    svc_port = coap_port
    svc_props = {"url": coap_url}
    svc_server = instance + "." + domain

    srv = zeroconf.ServiceInfo(svc_type, svc_name, svc_addr, svc_port, properties=svc_props, server=svc_server)
    zconf = zeroconf.Zeroconf(interfaces=zeroconf.InterfaceChoice.Default)
    zconf.register_service(srv)


if __name__ == "__main__":
    main()