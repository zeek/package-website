"""
Retrieve content between brackets in toml styled files
"""
import re
import pandas as pd
import requests
# github supports base64 encoding
import base64



def parse(url):
    req = requests.get(url)

    regex_pkg = r'^\[(.*?)\]'
    regex_desc = r'^description\s+=\s+"(.*)"'
    
    pkgs = re.findall(regex_pkg, req.text, re.MULTILINE)
    
    for pkg in pkgs:
        pkg_desc = re.search(rf'^\[{pkg}\].*', req.text, re.MULTILINE)
        pkg_desc = pkg_desc.group(0) if pkg_desc else ''
        pkg_desc_match = re.search(regex_desc, pkg_desc, re.MULTILINE)
        pkg_desc_str = pkg_desc_match.group(1).strip() if pkg_desc_match else ''
        print(f"{pkg.strip()}: {pkg_desc_str}")



def main():
    url = 'https://raw.githubusercontent.com/zeek/packages/master/aggregate.meta'
    parse(url)

if __name__ == '__main__':
    main()

