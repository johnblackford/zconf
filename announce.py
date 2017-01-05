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