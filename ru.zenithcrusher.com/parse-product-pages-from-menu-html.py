import re

with open('source/product-links.txt', 'r', encoding='utf8') as f:
	html = f.read()

result = re.findall(r'https?://.*?\.html', html)
print(result)

with open('source/product-links-all.txt', 'w', encoding='utf8') as f:
	f.write('\n'.join(result))