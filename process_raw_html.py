from datetime import datetime
import re
import json

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

inputfile = open('gallup_data.html', 'r')
html = inputfile.read()
soup = BeautifulSoup(html, 'html.parser')

data = {}

for section in soup.find_all('tbody', attrs={'class': 'row-group'}):
    title = section.find('th', attrs={'scope': 'rowgroup'}).text
    print 'Title: [{}]'.format(title)

    years = []
    pct_pos_arr = []
    pct_neg_arr = []
    pct_depends_arr = []

    first_row = True
    for row in section.find_all('tr'):
        if first_row:
            first_row = False
            continue

        date = row.find('th', attrs={'scope': 'row'}).text
        year = re.sub(' .*', '', date)

        pct_positive = row.find(
            'td', attrs={'data-th': 'Morally acceptable'}).text
        pct_negative = row.find(
            'td', attrs={'data-th': 'Morally wrong'}).text
        pct_depends = row.find(
            'td', attrs={'data-th': 'Depends (vol.)'}).text

        if pct_depends == '*':
            pct_depends = 0

        print '\t{} - Good:{}% Bad:{}% Depends:{}%'.format(
            year, pct_positive, pct_negative, pct_depends)

        years.insert(0,int(year))
        pct_pos_arr.insert(0,int(pct_positive))
        pct_neg_arr.insert(0,int(pct_negative))
        pct_depends_arr.insert(0,int(pct_depends))

    if len(years) > 1:
      data[title] = {
          'years': years,
          'good': pct_pos_arr,
          'bad': pct_neg_arr,
          'depends': pct_depends_arr
      }

with open('data.js', 'w') as outfile:
    jsonstr = json.dumps(data)
    outfile.write("var data = {}".format(jsonstr))
