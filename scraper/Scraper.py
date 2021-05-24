import os
import csv
import requests
from bs4 import BeautifulSoup
import re
#from concurrent.futures import ProcessPoolExecutor as PoolExecutor
import time
from requests_html import HTMLSession

def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01'}
    url = url.strip()
    response = requests.get(url, timeout=10, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    fileName = re.sub('https://www.iasg.com/en-us/groups/group/', '', url)
    fileName = re.sub('/', '.', fileName)
    with open('..//data//' + fileName + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        session = HTMLSession()
        r = session.get(url)
        r.html.render(timeout=30, sleep=10)
        tableCalendar = r.html.find('table', first=True)
        if tableCalendar is None:
            os.remove('..//data//' + fileName + '.csv')
            return
        strList = tableCalendar.text.split('\n')
        str=''
        for index in range(0, len(strList)):
            if index % 15 == 0 and index != 0:
                str += '\n' + strList[index]+' '
            else:
                str += strList[index] + ' '
        strList = str.split('\n')
        for s in strList:
            writer.writerow([s])
        tables = soup.find_all('table')
        for table in tables:
            if table != soup.find('table', class_='performance-table responsive') and table not in soup.find_all('table', class_='minimal'):
                body = table.find('tbody')
                head = table.find('thead')
                if head is not None:
                    headRow = head.find('tr')
                    headColumns = headRow.find_all('th')
                    str=''
                    for col in headColumns:
                        str+=col.text.strip()+' '
                    writer.writerow([str])
                rows = body.find_all('tr')
                for row in rows:
                    columns = row.find_all('th')
                    dinColumns = row.find_all('td')
                    str = ''
                    for col in columns:
                        str+=col.text.strip()+' '
                    for col in dinColumns:
                        str+=col.text.strip()+' '
                    writer.writerow([str])
        strategy = soup.find_all('div', class_='span-1-1-2-desktop performance-summary')[1]
        if strategy is not None:
            dtStrategy = strategy.find_all('dt')
            ddStrategy = strategy.find_all('dd')
            if dtStrategy is not None and ddStrategy is not None:
                for dt, dd in zip(dtStrategy, ddStrategy):
                    a = dt.find('a')
                    writer.writerow([a.text.strip()+' '+dd.text.strip()])
        composition = soup.find_all('div', class_='span-1-2-2-desktop performance-summary')[1]
        if composition is not None:
            dtComposition = composition.find_all('dt')
            ddComposition = composition.find_all('dd')
            if dtComposition is not None and ddComposition is not None:
                for dt, dd in zip(dtComposition, ddComposition):
                    a = dt.find('a')
                    writer.writerow([a.text.strip()+' '+dd.text.strip()])
        risks = soup.find('div', class_='span-1-3-4-desktop performance-summary')
        if risks is not None:
            dtRisks = risks.find_all('dt')
            ddRisks = risks.find_all('dd')
            if dtRisks is not None and ddRisks is not None:
                for dt, dd in zip(dtRisks, ddRisks):
                    writer.writerow([dt.text.strip()+' '+dd.text.strip()])
        asserts = soup.find('div', class_='span-1-4-4-desktop performance-summary')
        if asserts is not None:
            dtAsserts = asserts.find_all('dt')
            ddAsserts = asserts.find_all('dd')
            if dtAsserts is not None and ddAsserts is not None:
                for dt, dd in zip(dtAsserts, ddAsserts):
                    writer.writerow([dt.text.strip()+' '+dd.text.strip()])

if __name__=="__main__":
    start_time = time.time()
    with open('links.txt', 'r') as f:
        urls = f.read().splitlines()
        #with PoolExecutor(max_workers=16) as executor:
        #    for index, value in enumerate(executor.map(scrape_data, urls)):
        #        print(f'{index} {urls[index]}')
        #        pass
        for index in range(2, len(urls)):
            print(f'{index} {urls[index]}') 
            scrape_data(urls[index])
    print("--- %s seconds ---" % (time.time() - start_time))

