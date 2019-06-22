from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

configs = {'F/mph': 'us12', 'C/ms': 'si12', 'C/kmh': 'ca12', 'C/mph': 'uk212'}


def get_forcast(latitude, longitude, config_mode='C/ms'):

    page = urlopen(f'https://darksky.net/forecast/{latitude},{longitude}/{configs[config_mode]}/en')
    soup = BeautifulSoup(page, 'html.parser')

    temp_dict = {}
    for temp in soup.find_all('span', attrs={'class': 'high-low-label'}):
        if temp.text == 'Low: ':
            temp_dict['low'] = float(re.findall(r'\d+', temp.parent.text)[0])
        elif temp.text == 'High: ':
            temp_dict['high'] = float(re.findall(r'\d+', temp.parent.text)[0])
        elif temp.text == 'Feels Like: ':
            temp_dict['feels like'] = float(re.findall(r'\d+', temp.parent.text)[0])

    details = {}
    for div in soup.find('div', attrs={'id': 'currentDetails'}).find_all('div'):    
        if div['class'][0] != 'current_details_break':
            details[div['class'][0]] = {}
            if (div.find('span', attrs={'class': 'num swip'})) != None:
                details[div['class'][0]]['value'] = float(div.find('span', attrs={'class': 'num swip'}).text)
            else:
                if (div.find('span', attrs={'class': 'val swap'})) != None:
                    details[div['class'][0]]['value'] = float((div.find('span', attrs={'class': 'val swap'})).find('span', attrs={'class': 'num'}).text)

            if (div.find('span', attrs={'class': 'unit swap'})) != None:
                details[div['class'][0]]['unit'] = div.find('span', attrs={'class': 'unit swap'}).text
            else:
                unit = (div.find('span', attrs={'class': 'val swap'})).find('span', attrs={'class': 'unit'})
                if unit != None:
                    details[div['class'][0]]['unit'] = unit.text
                else:
                    details[div['class'][0]]['unit'] = None


    for script in soup.find_all("script", {"src":False}):
        if script:
            values = re.findall(r'var.*?=\s*(.*?);', script.text, re.DOTALL | re.MULTILINE)
            for value in values:
                vals = ({key: eval(val) for key, val in [x.split('=') for x in ('latitude=' + value.replace(' ', '').replace(',\n', '\n').replace('false', 'False').replace('true', 'True').replace('null', '"Null"')).split('\n')]})

    return {'temperatures': temp_dict, 'weather data': details, 'all data': vals}        

def overtime_forcast(latitude, longitude, config_mode='C/ms'):
    page = urlopen(f'https://darksky.net/forecast/{latitude},{longitude}/{configs[config_mode]}/en')
    soup = BeautifulSoup(page, 'html.parser')
    for script in soup.find_all("script", {"src":False}):
        if script:
            values = re.findall(r'var.*?=\s*(.*?);', script.text, re.DOTALL | re.MULTILINE)
            for value in values:
                vals = ({key: eval(val) for key, val in [x.split('=') for x in ('latitude=' + value.replace(' ', '').replace(',\n', '\n').replace('false', 'False').replace('true', 'True').replace('null', '"Null"')).split('\n')]})
    #vals['hour'] = [timeBlock ]
    for timeBlock in vals['hours']:
        timeBlock['epoch time'] = timeBlock['time']
        timeBlock['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeBlock['epoch time']))
       
    return vals['hours']

if __name__ == '__main__':
    #
    # Tested Origin Release Working: Fri 21 June 2019
    #
    latitude, longitude = 53.1058, -2.0243
    config_mode = 'C/ms'

    print(get_forcast(latitude, longitude, config_mode=config_mode))
    print(overtime_forcast(latitude, longitude, config_mode=config_mode))