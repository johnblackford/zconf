import argparse
import socket
import zeroconf


class MulticastDnsListener(object):
    def add_service(self, zconf, type, name):
        info = zconf.get_service_info(type, name)

        if info.type.endswith("_usp-agt-coap._udp.local."):
            addr = socket.inet_ntoa(info.address)
            port = str(info.port)
            print("Found a USP CoAP Agent: coap:\\\\" + addr + ":" + port + "\\usp")
            coap_url = info.properties.get(b'url', b'UNKNOWN').decode('ascii')
            print("Found a USP CoAP Agent at " + coap_url)

        print("Service [{}] was Added: {}".format(name, info))

    def remove_service(self, zconf, type, name):
        print("Service [{}] was Removed".format(name))



def main():
    browser = None
    parser = argparse.ArgumentParser()
    zconf = zeroconf.Zeroconf(interfaces=zeroconf.InterfaceChoice.Default)

    parser.add_argument("-s", "--service", action="store", nargs="?",
                        default="_http._tcp.local.",
                        help="listen for mDNS advertisements on the specified Service")
    args = parser.parse_args()

    service = args.service

    try:
        listener = MulticastDnsListener()
        browser = zeroconf.ServiceBrowser(zconf, service, listener)
        input("Press Enter to Continue...\n\n")
    finally:
        browser.cancel()
        zconf.close()


if __name__ == "__main__":
    main()