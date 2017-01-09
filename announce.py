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
import argparse
import zeroconf


_NAME_ = "Test Name"
_IP_ADDR_ = "127.0.0.1"
_AGENT_COAP_PORT_ = 15683
_CONTROLLER_COAP_PORT_ = 5683
_AGENT_SVC_NAME_ = "_usp-agt-coap._udp."
_CONTROLLER_SVC_NAME_ = "_usp-ctl-coap._udp."
_AGENT_ENDPOINT_ID_ = "00D09E-RPi_Test-T0000000001"
_CONTROLLER_ENDPOINT_ID_ = "controller-coap-johnb"
_COAP_RESOURCE_ = "usp"


def main():
    service = None
    instance = None
    coap_port = None
    svc_props = None
    domain = "local."
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--agent", action="store_true",
                        help="announce mDNS for a USP Agent")
    parser.add_argument("-c", "--controller", action="store_true",
                        help="announce mDNS for a USP Controller")
    args = parser.parse_args()
    is_agent = args.agent
    is_controller = args.controller

    if is_agent:
        coap_port = _AGENT_COAP_PORT_
        instance = _AGENT_ENDPOINT_ID_
        service = _AGENT_SVC_NAME_
        svc_props = {"path": _COAP_RESOURCE_, "name": _NAME_}

    if is_controller:
        coap_port = _CONTROLLER_COAP_PORT_
        instance = _CONTROLLER_ENDPOINT_ID_
        service = _CONTROLLER_SVC_NAME_
        svc_props = {"path": _COAP_RESOURCE_}

    svc_type = service + domain
    svc_name = instance + "." + service + domain
    svc_addr = socket.inet_aton(_IP_ADDR_)
    svc_port = coap_port
    svc_server = instance + "." + domain

    srv = zeroconf.ServiceInfo(svc_type, svc_name, svc_addr, svc_port, properties=svc_props, server=svc_server)
    zconf = zeroconf.Zeroconf(interfaces=zeroconf.InterfaceChoice.Default)
    zconf.register_service(srv)

    try:
        input("Press Enter to Continue...\n\n")
    finally:
        zconf.close()



if __name__ == "__main__":
    main()