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
            self._print_agent_info(info)
        elif info.type.endswith("_usp-ctl-coap._udp.local."):
            self._print_controller_info(info)

        print("")
        print("Service [{}] was Added: {}".format(name, info))

    def remove_service(self, zconf, type, name):
        print("Service [{}] was Removed".format(name))


    def _print_coap_url(self, info, addr_type):
        print("Found a USP CoAP {}".format(addr_type))
        resource_path = info.properties.get(b'path')

        if resource_path is not None:
            addr = socket.inet_ntoa(info.address)
            port = str(info.port)
            decoded_resource_path = resource_path.decode('ascii')
            coap_url = "coap://" + addr + ":" + port + "/" + decoded_resource_path
            print(" -- The {}'s CoAP URL is: {}".format(addr_type, coap_url))
        else:
            print(" -- The {}'s CoAP URL could not be determined".format(addr_type))

    def _print_agent_info(self, info):
        name = info.properties.get(b'name')
        self._print_coap_url(info, "Agent")

        if name is not None:
            decoded_name = name.decode('ascii')
            print(" -- The Agent's CoAP Friendly Name is: {}".format(decoded_name))
        else:
            print(" -- The Agent's CoAP Friendly Name was not found")

    def _print_controller_info(self, info):
        self._print_coap_url(info, "Controller")


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