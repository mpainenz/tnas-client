# TNAS-Client
This project contains a very simple, easy to use, TNAS API Client written in Python 3.6.

TNAS is used for Toll Free Number Portability in New Zealand.

This library requires no third-party libraries, and supports TLS1.2 SSL. 

Currently this library only supports the Login functionality. If there is interest, I will look at adding other functions as required.

# Example code

In order to make things simple for those who aren't familiar with Programming, most of the more complicated code is wrapped inside a class called TNASConnection. You use this class to connect and run commands against TNAS. This means connecting to TNAS can be done in only three lines of code.

```sh
from connection import api_client
tnas_connection = api_client.TNASConnection(api_client.TNAS_TEST)
tnas_connection.login(username='aperson', password='apassword', carrier_id='12345')
```



# Installation

For Windows users:
  - Install [Python 3.6](https://www.python.org/downloads/release/python-360/) or later
  - Clone this library using a Git client, such as [TortoiseGit](https://tortoisegit.org/) for Windows (Or simply download using the green link above)
  - You can then either use Python from command line to execute the example.py script, or I would recommend using an IDE like PyCharm which is a lot more user-friendly


# Usage

For a basic example, look at the [example.py](example.py) script.

Simply change the Username, Password, and Carrier ID fields to something valid, and run the script to connect to TNAS

