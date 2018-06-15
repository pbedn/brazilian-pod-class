import json
from collections import defaultdict

from requests_html import HTMLSession

url = "https://web.archive.org/web/20170621070901/http://www.brazilianpodclass.com:80/smart-search/"
bad_url = 'https://web.archive.org/web/20170621070901/'

# Make a GET request
session = HTMLSession()
r = session.get(url)

# Select text inside <div id='tabs-6'>
tab = r.html.find("#tabs-6", first=True)
text = tab.text

# Select <h3> element
header = tab.find('h3', first=True).text

header_remove = header + "\n"
text = tab.text.replace(header_remove, "")

# Select and clean text inside <h5>
levels = [l.text for l in tab.find('h5')]
for level in reversed(levels):
    level_remove = level + "\n"
    text = text.replace(level_remove, "")

text_split_into_levels = [t.split("\n") for t in text.split("\n\n\n")]

# Select text and links inside <li>
raw_data = [(t.text, list(t.links)[0].replace(bad_url, "")) for t in tab.find('li')]

dct = defaultdict(list)

# Iterate and sort raw_data into levels
for i, v in enumerate(levels):
    for d in raw_data:
        if d[0] in text_split_into_levels[i]:
            dct[v.replace(" ", "_")].append(d)


with open('data.json', 'w', encoding='utf-8') as fout:
    json.dump(dct, fout, ensure_ascii=False, indent=2)
