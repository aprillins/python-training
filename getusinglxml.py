from lxml import html
import requests

page = requests.get('https://www.mpasi.org/')
tree = html.fromstring(page.content)
title = tree.xpath('//title/text()')
meta_description = tree.xpath('//meta[@name="description"]/@content')
links = tree.xpath('//a')

print('Title:', title)
print('Meta description:', meta_description)
print('Total links:', links.count())
