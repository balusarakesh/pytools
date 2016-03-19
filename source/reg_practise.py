import re

line = 'imageine a new world by rakesh ';
pattern = re.compile(r'(\w+) (\w+)')
val =  pattern.finditer(line)
print val.next().group(2)
print val.next().group(1)
print val.next().group()

