import csv
import requests
from bs4 import BeautifulSoup
import re
#from concurrent.futures import ThreadPoolExecutor as PoolExecutor
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
    with open(fileName + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        session = HTMLSession()
        r = session.get(url)
        r.html.render(timeout=30, sleep=10)
        tableCalendar = r.html.find('table', first=True)
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
            if table != soup.find('table', class_='performance-table responsive'):
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

if __name__=="__main__":
    start_time = time.time()
    with open('links.txt', 'r') as f:
        urls = f.read().splitlines()
        #with PoolExecutor(max_workers=4) as executor:
        #    for index, value in enumerate(executor.map(scrape_data, urls)):
        #        print(index+' '+value)
        #        pass
        for index in range(365,len(urls)):
            print(f'{index} {urls[index]}')
            scrape_data(urls[index])
    print("--- %s seconds ---" % (time.time() - start_time))

