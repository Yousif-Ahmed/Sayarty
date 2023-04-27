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
from deep_translator import GoogleTranslator

KEYS_MAPPING = {
    'Make': 'الماركة',
    'Model': 'الموديل',
    'Used since' : 'أول استخدام',
    'Km': 'العداد',
    'Fuel': 'نوع الوقود',
    'Transmission': 'ناقل الحركة',
    'Color': 'اللون',
    'City': 'المحافظة',
    'Price': 'price',
    'Engine': 'سعة المحرك',
    'Body': 'نوع الهيكل',
}

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
    grids = soup.find_all('div', class_='used_grid_container')
    ads = []
    for grid in grids:
        ads += grid.find_all('h2', class_='mb-2 mb-md-3')
    links = []
    for ad in ads:
        a = ad.find('a').get('href')
        link =  a
        links.append(link)
    return links

# Get the data of each car
def get_car_data(html):
    translator = GoogleTranslator(source='auto', target='en')

    data = {}
    soup = BeautifulSoup(html, 'lxml')
    
    dataitems_1 = soup.find('div', class_='car_data p-3 pt-3 pb-3').findAll('div', class_='row gap-3 mt-3')
    dataitems_2 = soup.find('div', class_='car_data p-3 pt-3 pb-3').findAll('div', class_='col bg-light rounded p-2')
    dataitems = dataitems_1 + dataitems_2

    for i in range(len(dataitems)):
        try:
            key = dataitems[i].find('span',class_= 'd-block font-sm').text.strip()
            value = dataitems[i].find('span',class_= 'fw-600').text.strip()
            # check if the string not have numbers 
            if not any(char.isdigit() for char in value):
                value = translator.translate(value)
            data[key] = value
        except:
            pass    
    
    # getting price value form another div  
    try: 
        data['price'] = soup.find('div', class_='row align-items-center justify-content-between justify-content-md-end').find('span', class_ ='h2 mb-0 text-muted fw-800 col-auto').text.strip()
    except:
        data['price'] = None   
    

    data = {
                'brand': data[KEYS_MAPPING['Make']] if KEYS_MAPPING['Make'] in data else None ,
                'model': data[KEYS_MAPPING['Model']] if KEYS_MAPPING['Model'] in data else None,
                'year': data[KEYS_MAPPING['Used since']] if KEYS_MAPPING['Used since'] in data else None,
                'price': data[KEYS_MAPPING['Price']] if KEYS_MAPPING['Price'] in data else None,
                'mileage': data[KEYS_MAPPING['Km']] if KEYS_MAPPING['Km'] in data else None,
                'fuel': data[KEYS_MAPPING['Fuel']] if KEYS_MAPPING['Fuel'] in data else None,
                'gear': data[KEYS_MAPPING['Transmission']] if KEYS_MAPPING['Transmission'] in data else None,
                'color': data[KEYS_MAPPING['Color']] if KEYS_MAPPING['Color'] in data else None,
                'city': data[KEYS_MAPPING['City']] if KEYS_MAPPING['City'] in data else None,
                'engine': data[KEYS_MAPPING['Engine']] if KEYS_MAPPING['Engine'] in data else None,
                'body': data[KEYS_MAPPING['Body']]  if KEYS_MAPPING['Body'] in data else None,
            }
    return data

# Save the data in csv file
def save_file(items= None, path= None, headers=False):
    with open(path, 'a') as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(['Brand', 'Model','Color','Year','Fuel','Kilometes', 'Trasmission', 'Price', 'Gov' , 'Engine', 'Body'])
        else:    
            writer.writerow([items['brand'],
                            items['model'],
                            items['color'],                            
                            items['year'],
                            items['fuel'],
                            items['mileage'],
                            items['gear'],
                            items['price'],
                            items['city'],
                            items['engine'],
                            items['body']])

def main():

    url = 'https://malekcars.com/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%85%D8%B3%D8%AA%D8%B9%D9%85%D9%84%D8%A9/'
    base_url = 'https://malekcars.com/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%85%D8%B3%D8%AA%D8%B9%D9%85%D9%84%D8%A9/page/'
    # total_pages = get_total_pages(get_html(url))
    total_pages = 112
    
    get_page_data(get_html(url))
    # writing file headers

    save_file(path='cars.csv', headers=True)
    for i in range(1, total_pages + 1):
        url_gen = base_url + str(i) 
        html = get_html(url_gen)
        links = get_page_data(html)
        for link in links:
            print(link)
            html = get_html(link)
            data = get_car_data(html)
            save_file(data, 'cars.csv')
            

if __name__ == '__main__':

    main()