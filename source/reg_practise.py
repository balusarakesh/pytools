import re

line = 'aba';
pattern = re.compile(r'ab*')
print pattern.findall(line)

