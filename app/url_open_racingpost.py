#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def url_open(url):
    '''
    Extract raw_html data using requests and 
    return the nicely formatted BeautifulSoup object
    for the given url
    '''
    headers = {'user-agent': 'Magic Browser'}
    req = requests.get(url, headers=headers)
    response = req.content
    soup = BeautifulSoup(response, "html.parser")
   
    page = soup.find_all("td")
    el_id = 0
    group_counter = 0
    sql_values = ''
    first_value = True
    for element in page:
        el_id = el_id + 1
        if element.has_attr('colspan'):
            if int(element["colspan"]) == 12:
                el_id = 0
                group_counter += 1
                if group_counter > 17:
                    sql_values += ');'
                elif sql_values != '(DEFAULT':
                    sql_values += ')'
                    print(group_counter)
        if el_id == 1:
            if first_value:
                sql_values += "\n(DEFAULT, '%(e)s'" % {"e": element.get_text().strip()}
                first_value = False
            else:
                sql_values += ",\n(DEFAULT, '%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 2:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip().split(' ')[0]}
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip().split(' ')[1]}
        elif el_id == 3:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 4:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 5:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 6:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 7:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 8:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 9:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 10:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
        elif el_id == 11:
            sql_values += ",'%(e)s'" % {"e": element.get_text().strip()}
    sql_values += ';'
    print(sql_values)
    return soup

if __name__ == '__main__':
    url = 'http://www.racingpost.com/horses/result_home.sd?race_id=600011'
    url_open(url)
