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


def read_pct_int(row, header):
    text = row.find('td', attrs={'data-th': header}).text
    if text == '*':
        return 0
    return int(text)


for section in soup.find_all('tbody', attrs={'class': 'row-group'}):
    title = section.find('th', attrs={'scope': 'rowgroup'}).text
    print 'Title: [{}]'.format(title)

    years = []
    pct_pos_arr = []
    pct_neg_arr = []
    pct_other_arr = []

    first_row = True
    for row in section.find_all('tr'):
        if first_row:
            first_row = False
            continue

        date = row.find('th', attrs={'scope': 'row'}).text
        year = re.sub(' .*', '', date)

        pct_positive = read_pct_int(row, 'Morally acceptable')
        pct_negative = read_pct_int(row, 'Morally wrong')
        pct_depends = read_pct_int(row, 'Depends (vol.)')
        pct_no_opinion = read_pct_int(row, 'No opinion')
        pct_other = pct_depends+pct_no_opinion

        print '\t{} - Good:{}% Bad:{}% Depends:{}%'.format(
            year, pct_positive, pct_negative, pct_depends)

        years.insert(0, year)
        pct_pos_arr.insert(0, pct_positive)
        pct_neg_arr.insert(0, pct_negative)
        pct_other_arr.insert(0, pct_depends+pct_no_opinion)

    if len(years) > 1:
        data[title] = {
            'years': years,
            'good': pct_pos_arr,
            'bad': pct_neg_arr,
            'other': pct_other_arr
        }

with open('data.js', 'w') as outfile:
    jsonstr = json.dumps(data)
    outfile.write("var data = {}".format(jsonstr))
