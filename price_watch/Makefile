#!/usr/bin/env make


.PHONY: install
install: 
	pip3 install beautifulsoup4
	pip3 install pandas
	pip3 install nextcord
	pip3 install scrapingant_client
	pip3 install fake-useragent


.PHONY: build
build: 



.PHONY: test
test: 
	python3 -m unittest test/test_getPrice.py


.PHONY: clean
clean: 
	rm -rf ./libs ./package


.PHONY: pack
pack: 
	pip3 install --target ./libs requests beautifulsoup4 pandas fake_useragent
	mkdir package	
	cd libs && zip -r ../package/lambda_service_price_checker.zip .
	zip -g package/lambda_service_price_checker.zip index.py program/*.*

