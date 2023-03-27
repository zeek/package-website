import re

with open('file.txt', 'r') as f:
    package_entries = f.read()

pattern = r"description = (.*)\n"

descriptions = re.findall(pattern, package_entries)
print(descriptions)
print('\n')

