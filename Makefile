.PHONY: schema

init:
	pip install --upgrade pip
	pip install -r requirements.txt

find:
	python3 -m find

listen:
	python3 -m listen -s _usp-agt-coap._udp.local.

announce:
	python3 -m announce
