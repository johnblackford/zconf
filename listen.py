# Copyright (c) 2016 John Blackford
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import socket
import zeroconf


class MulticastDnsListener(object):
    def add_service(self, zconf, type, name):
        info = zconf.get_service_info(type, name)

        if info.type.endswith("_usp-agt-coap._udp.local."):
            print("Found a USP CoAP Agent")
            coap_url = info.properties.get(b'url').decode('ascii')

            if coap_url is not None:
                print(" -- The Agent's CoAP URL is: " + coap_url)
            else:
                addr = socket.inet_ntoa(info.address)
                port = str(info.port)
                print(" -- The Agent's CoAP URL Should be: coap:\\\\" + addr + ":" + port + "\\usp")

        print("")
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