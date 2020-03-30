import os
import datetime
import requests
import pandas as pd
from requests_html import HTML

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
# BASE_DIR = os.path.dirname(__file__)

def url_to_txt(url, filename='world.html', save=False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f'world-{year}.html', 'w') as f:
                f.write(html_text)
        return html_text
    return ''


def parse_and_extract(url, name='2020'):
    html_text = url_to_txt(url)

    r_html = HTML(html=html_text)
    table_class = '.imdb-scroll-table'
    r_table = r_html.find(table_class)

    table_data = []
    header_names = []
    if len(r_table) == 1:
        parsed_table = r_table[0]
        rows = parsed_table.find('tr')
        header_row = rows[0]
        header_cols = header_row.find('th')
        header_names = [x.text for x in header_cols]

        for row in rows[1:]:
            print(row.text)
            cols = row.find('td')
            row_data = []
            for i, col in enumerate(cols):
                print(i, col.text, '\n\n')
                row_data.append(col.text)
            table_data.append(row_data)
        df = pd.DataFrame(table_data, columns=header_names)
        path = os.path.join(BASE_DIR, 'data')
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(BASE_DIR, 'data', f'{name}.csv')
        df.to_csv(filepath, index=False)


def run(start_year=None, years_ago=10):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f'{start_year}') == 4

    for i in range(0, years_ago+1):
        url = f'https://www.boxofficemojo.com/year/world/{start_year}/'
        parse_and_extract(url, name=start_year)
        start_year -= 1


if __name__ == '__main__':
    run()



