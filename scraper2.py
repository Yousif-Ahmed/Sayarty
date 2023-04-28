'''
This script used to scarp Hatla2ee website https://eg.hatla2ee.com/en/car
We extract used cars data from this website and save it in csv file
Mainly we are interested in the following fields:
- Brand
- Model
- Year
- Price
- Mileage
- Fuel
- Gear
- Color
- City
'''

import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

# Get the html content of the page
def get_html(url):
    r = requests.get(url)
    return r.text

# Get the total number of pages
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination pagination-right').find_all('ul')[0].find_all('li')[-2].find('a').get('href')
    total_pages = pages.split('/')[-1]
    return int(total_pages)

# Get the links of all cars in the page
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='CarListWrapper').find_all('div', class_='newCarListUnit_contain')
    links = []
    for ad in ads:
        a = ad.find('div', class_='newCarListUnit_wrap').find('div', class_='newCarListUnit_data_wrap').find('div', class_='newCarListUnit_data_contain').find('div', class_='newCarListUnit_header').find('a').get('href')
        link = 'https://eg.hatla2ee.com' + a
        links.append(link)
    return links

# Get the data of each car
def get_car_data(html):
    data = {}
    soup = BeautifulSoup(html, 'lxml')
    
    dataitems = soup.find('div', class_='DescDataContain').findAll('div', class_='DescDataItem')

    for i in range(len(dataitems)):
        try:
            key = dataitems[i].find('span',class_= 'DescDataSubTit').text.strip()
            value = dataitems[i].find('span',class_= 'DescDataVal').text.strip()
            data[key] = value
        except:
            pass  

    # getting price value form another div  
    try: 
        data['price'] = soup.find('div', class_='usedUnitPriceNumb').find('span', class_ ='usedUnitCarPrice').text.strip()
    except:
        data['price'] = None   
    
    data = {
                'brand': data['Make'],
                'model': data['Model'],
                'year': data['Used since'],
                'price': data['price'],
                'mileage': data['Km'],
                'fuel': data['Fuel'],
                'gear': data['Transmission'],
                'color': data['Color'],
                'city': data['City']
            }
    return data

# Save the data in csv file
def save_file(items= None, path= None, headers=False):
    with open(path, 'a') as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(['Brand', 'Model','Color','Year','Fuel','Kilometes', 'Trasmission', 'Price', 'Gov'])
        else:    
            writer.writerow([items['brand'],
                            items['model'],
                            items['color'],                            
                            items['year'],
                            items['fuel'],
                            items['mileage'],
                            items['gear'],
                            items['price'],
                            items['city']])

def main():
    url = 'https://eg.hatla2ee.com/en/car'
    base_url = 'https://eg.hatla2ee.com/en/car/page/'
    total_pages = get_total_pages(get_html(url))
    print(total_pages)
    get_page_data(get_html(url))
    # writing file headers
    save_file(path='cars2.csv', headers=True)
    for i in tqdm(range(126, total_pages + 1)):
        url_gen = base_url + str(i) 
        html = get_html(url_gen)
        links = get_page_data(html)
        for link in links:
            html = get_html(link)
            data = get_car_data(html)
            save_file(data, 'cars2.csv')
            


if __name__ == '__main__':
    main()