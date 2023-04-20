# Price match application

## Introduction

A program allow user to trake the price of the produce they are insterested, by given a url a price shall returned. 

The program should run daily until a price change has been found and user will be notify. The program aim to inform user to ....

## File structure

### Program files

The program files consist of:
	user_friendly.py -- put all function together and interact with user by CLI
	getPrice.py -- Given a URL, and get the current price on the page and store/update it in search_result.json
	searchPrice.py -- Given a URL, and current price on the page, and save 'data' to  search_path.json

### Data files

data files are:
	search_path.json -- a dictionary consist of web domain as key and search index and strings to locate the price
	search_result.json -- a data dictionary consist of url and prices infomation

## How to install

Run `make install` to install all required python packages

## How to run

run python file main.py; This can be achieved by execute in a IDE such as vscode.
anthor way to run is by open terminal, cd to the project's directory run command

``` bash
python3 program/user_friendly.py
```

at the moment only `example_user1@gamil.com` is vaild email

## Reference

Recommand to install SciTE https://www.scintilla.org/index.html 
a small but helpful tool to view and edit .json 

Recommand to install chromedriver from this link, pls check the version for ur chrome
https://chromedriver.chromium.org/downloads #forget about selenium for now
