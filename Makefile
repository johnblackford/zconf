.PHONY: schema

init:
	pip install --upgrade pip
	pip install -r requirements.txt

find:
	python3 -m find

listen-agent:
	python3 -m listen -s _usp-agt-coap._udp.local.

listen-controller:
	python3 -m listen -s _usp-ctl-coap._udp.local.

announce-agent:
	python3 -m announce -a

announce-controller:
	python3 -m announce -c
