"""
Downloads all datasets from data.gov.in into a datasets/ folder
"""
import os
import urllib
import lxml.html

catalog = urllib.urlopen(
    'http://data.gov.in/catalogs/?' + urllib.urlencode({
        'filter' : 'catalog_type:catalog_type_raw_data',
        'sort'   : 'recent desc',
        'results': 9999,
    }),
)

folder = 'datasets'
if not os.path.exists(folder):
    os.makedirs(folder)

tree = lxml.html.parse(catalog)
for tr in tree.findall('.//tbody//tr'):
    td = tr.findall('.//td')
    title = td[1].find('.//a')
    download = td[-1].find('.//a')
    base = title.get('href').split('/')[-1]
    ext = download.find('.//img').get('src').split('/')[-1].split('.')[0]
    filename = os.path.join(folder, base + '.' + ext)
    if not os.path.exists(filename):
        print filename
        urllib.urlretrieve(download.get('href'), filename)
