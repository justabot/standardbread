#!/usr/bin/env python3

import time
import requests
from bs4 import BeautifulSoup
import psycopg2

def url_open(url):
	conn_string = "host='localhost' dbname='standardbread' user='sb_app' password='febreeze'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM track")
	records = cursor.fetchall()

	for rec in records:
		date_str = ''
		month = 7
		day = 17
		race_types = ["n","q","s","a"]
		while month < 8:
			while day < 32:
				if day < 10:
					date_str = '0%(m)s0%(d)s' % {"m": month, "d": day}
				else:
					date_str = '0%(m)s%(d)s' % {"m": month, "d": day}
				for race_type in race_types:
					race_ident = 'r%(d)s%(r)s%(t)s' % \
					{"d": date_str, "r": rec[2], "t": race_type}
					formatted_url = url + race_ident + '.dat'
					print(formatted_url)
					headers = {'user-agent': 'Magic Browser'}
					req = requests.get(formatted_url, headers=headers)
					response = req.content
					soup = BeautifulSoup(response, "html.parser")
					page = soup.find_all("pre")					
					sql_values = ''
					first_value = True
					sql_columns = "\
						DELETE FROM race \
						 WHERE track_id = %(t)s \
						   AND race_date = '%(d)s'; \
						INSERT INTO race VALUES " %	{"t": rec[0], "d": date_str}		
					for element in page:
						if first_value:
							sql_values += "\n(DEFAULT, '%(t)s', '%(d)s', '%(e)s')" % \
							{"t": rec[0], "d": date_str, "e": element.get_text()}
							first_value = False
						else:
							sql_values += ",\n(DEFAULT, '%(t)s', '%(d)s', '%(e)s')" % \
							{"t": rec[0], "d": date_str, "e": element.get_text()}
					conn_insert = psycopg2.connect(conn_string)
					cur_insert = conn_insert.cursor()
					insert_query = '%(c)s%(v)s;' % {"c": sql_columns, "v": sql_values}
					try:
						cur_insert.execute(insert_query)
					except Exception as e:
						print(e)
						continue
					conn_insert.commit()						
					cur_insert.close()
					conn_insert.close()
				day += 1
				time.sleep(6)
			month += 1

	return soup

if __name__ == '__main__':
	url = 'http://www.standardbredcanada.ca/racing/results/data/'
	url_open(url)