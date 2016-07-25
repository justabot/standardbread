#!/usr/bin/env python3

import time
import requests
from bs4 import BeautifulSoup
import psycopg2

def url_open(url):
	conn_string = "host='localhost' dbname='standardbread' user='sb_app' password='febreeze'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM track WHERE country = 'Australia'")
	records = cursor.fetchall()

	for rec in records:
		date_str = ''
		month = 7
		day = 17
		year = 11
		# while year < 17:
		# 	while month < 13:
		# 		while day < 32:
		if day < 10 and month < 10:
			date_str = '0%(d)s0%(m)s%(y)s' % {"m": month, "d": day, "y": year}
		elif day < 10:
			date_str = '0%(d)s%(m)s%(y)s' % {"m": month, "d": day, "y": year}
		elif month < 10:
			date_str = '%(d)s0%(m)s%(y)s' % {"m": month, "d": day, "y": year}
		else:
			date_str = '%(d)s%(m)s%(y)s' % {"m": month, "d": day, "y": year}

		day += 1
		race_ident = '%(r)s%(d)s' % \
		{"d": date_str, "r": rec[2]}
		# formatted_url = url + race_ident
		formatted_url = url + 'BH180516'
		print(formatted_url)
		headers = {'user-agent': 'Magic Browser'}
		req = requests.get(formatted_url, headers=headers)
		response = req.content
		soup = BeautifulSoup(response, "html.parser")
		# print(soup)
		page = soup.find_all("table", attrs={'class':'race_field_table'})	
		
		for rows in page:
			for row in rows.find_all('tr'):
				# for headers in row.find_all('th'):

				for cols in row.find_all('td')[0]:

					print('-----------')
					print(cols.get_text())
					print('-----------')
		# rows = table_body.find_all('tr')
		# for row in rows:
		#     cols = row.find_all('td')
		#     for col in cols:
		#     	print col.get_text()
		    # cols = [ele.text.strip() for ele in cols]
		    # data.append([ele for ele in cols if ele]) # Get rid of empty values
			
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
		sleep(800)
		conn_insert.commit()						
		cur_insert.close()
		conn_insert.close()
			# 	month += 1
			# 	day = 1
			# 	time.sleep(3)
			# year += 1
			# month = 1
			# day = 1



	return soup

if __name__ == '__main__':
	url = 'http://www.harness.org.au/meeting-results.cfm?mc='
	url_open(url)