"""
Retrieve content between brackets in toml styled files
"""
import re
import pandas as pd
import requests
# github supports base64 encoding
import base64

url = 'https://raw.githubusercontent.com/zeek/packages/master/aggregate.meta'
req = requests.get(url)

#print (req.text)

regex_title = r'^\[(.*?)\]' 

matches = re.findall(regex_title, req.text, re.MULTILINE)

#for match in matches:
#print(match.strip())
print(matches)





