.PHONY: schema

init:
	pip install --upgrade pip
	pip install -r requirements.txt

find:
	python3 -m find

la:
	python3 -m listen -s _usp-agt-coap._udp.local.

lc:
	python3 -m listen -s _usp-ctl-coap._udp.local.

aa:
	python3 -m announce -a

ac:
	python3 -m announce -c
