#!/usr/bin/env python3

import time
import requests
from bs4 import BeautifulSoup
import psycopg2
import pdb

def url_open(url):
	conn_string = "host='localhost' dbname='standardbread' user='sb_app' password='febreeze'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM track WHERE country = 'Australia' AND code = 'AP'")
	records = cursor.fetchall()

	for rec in records:
		date_str = ''
		# month = 7
		# day = 17
		# year = 16
		month = 8
		day = 16
		year = 16
		while year > 11:
			while month > 0:
				while day > 0:
					day -= 1
					if day < 10 and month < 10:
						date_str = '0%(d)s0%(m)s%(y)s' % {"m": month, "d": day, "y": year}
					elif day < 10 and month > 9:
						date_str = '0%(d)s%(m)s%(y)s' % {"m": month, "d": day, "y": year}
					elif month < 10 and day > 9:
						date_str = '%(d)s0%(m)s%(y)s' % {"m": month, "d": day, "y": year}
					else:
						date_str = '%(d)s%(m)s%(y)s' % {"m": month, "d": day, "y": year}

					race_ident = '%(r)s%(d)s' % \
					{"d": date_str, "r": rec[2]}
					formatted_url = url + race_ident
					print(formatted_url)
					headers = {'user-agent': 'Magic Browser'}
					req = requests.get(formatted_url, headers=headers)
					response = req.content
					soup = BeautifulSoup(response, "html.parser")
					# print(soup)
					time.sleep(1)
					page = soup.find_all("table", attrs={'class':'race_field_table'})	
					# print(page)
					place = 0
					horse_name = ''
					prize_money = ''
					row_bracket = ''
					horse_url = ''
					tab = ''
					trainer = ''
					driver = ''
					mgn = ''
					odds = 0
					comment = ''
					sql_columns = "INSERT INTO aus_race_details VALUES " 
					sql_values = ''	
					race_counter = 0
					row_index = 0
					# pdb.set_trace()
					page_id = 0
					page_length = (len(page)) 
					while page_id < page_length:
						conn_insert = psycopg2.connect(conn_string)
						cur_insert = conn_insert.cursor()
						time.sleep(1)
						first_value = True
						row_length = len(page[page_id].find_all("tr")) 
						row_id = 1
						while row_id < row_length:
							col_id = 0
							col_length = len(page[page_id].find_all("tr")[row_id].find_all("td")) 
							print('lengths: {0},{1},{2}'.format(page_length,row_length,col_length))
							col_count = 1		
							dat_count = 0	
							place_counter = 0	
							horse_named = False
							while col_id < col_length:
								col = page[page_id].find_all("tr")[row_id].find_all("td")[col_id]
								if col_count == 1:
									place_counter +=1
									if col.string:
										place = col.string.strip()
									if not place.isdigit():
										place = 31
									elif place == 1:
										race_counter += 1
								elif col_count == 2 + dat_count and not horse_named:
									if col.string:
										horse_name = col.string.strip()
									elif col.a.string:
										horse_name = col.a.string
									if col.a["href"]:
										horse_url = col.a["href"]
									if len(horse_name) < 1:
										dat_count = 1
									else:
										horse_named = True
								elif col_count == 3 + dat_count:
									if col.string:
										prize_money = col.string.replace('$','').replace(',','').strip()
									else:
										prize_money = 0
								elif col_count == 4 + dat_count:
									if col.string:
										row_bracket = col.string.strip()
									else:
										row_bracket = ''
								elif col_count == 5 + dat_count:
									if col.string:
										tab = col.string.strip()
									else:
										tab = ''
								elif col_count == 6 + dat_count:
									if col.string:
										trainer = col.string.strip()
									else:
										trainer = '';
								elif col_count == 7 + dat_count:
									if col.string:
										driver = col.string.strip()
									else:
										driver = ''
								elif col_count == 8 + dat_count:
									print(col)
									if col.string:
										mgn = col.string.strip()
									else:
										mgn = ''
								elif col_count == 9 + dat_count:
									if col.string:
										odds = col.string.replace('$','').replace('fav','').strip()
									else:
										odds = 0
									if not odds.isnumeric(): 
										odds = 0
								elif col_count == 11 + dat_count:
									if col.string:
										comment = col.string.strip()
									else:
										comment = ''									
								if not prize_money:
									prize_money = 0
								col_count += 1
								col_id += 1
							if first_value:
								sql_values = "\n(DEFAULT, $$%(ri)s$$, %(rn)s, %(p)s, $$%(h)s$$, '%(u)s', $aa$%(m)s$aa$, $$%(r)s$$,'%(t)s', $$%(a)s$$, $$%(d)s$$, $$%(g)s$$, %(o)s, '%(c)s')" \
									% {"ri": race_ident, "rn": race_counter, "p": place, "h": horse_name, "u": horse_url, "m": prize_money, "r": row_bracket, "t": tab, "a": trainer,
										 "d": driver, "g": mgn, "o": odds, "c": comment}
								first_value = False
							else:
								sql_values += ",\n(DEFAULT, $$%(ri)s$$, %(rn)s, %(p)s, $$%(h)s$$, '%(u)s', %(m)s, $$%(r)s$$,'%(t)s', $$%(a)s$$, $$%(d)s$$, $$%(g)s$$, %(o)s, '%(c)s')" \
									% {"ri": race_ident, "rn": race_counter, "p": place, "h": horse_name, "u": horse_url, "m": prize_money, "r": row_bracket, "t": tab, "a": trainer,
										 "d": driver, "g": mgn, "o": odds, "c": comment}
							row_id += 1
						page_id += 1
						insert_query = '%(c)s%(v)s;' % {"c": sql_columns, "v": sql_values}
						try:
							cur_insert.execute(insert_query)
						except Exception as e:
							print(e)
							continue
						conn_insert.commit()						
						cur_insert.close()
						conn_insert.close()
				month -= 1
				day = 32
			year -= 1
			month = 12
			day = 31



	return soup

if __name__ == '__main__':
	url = 'http://www.harness.org.au/meeting-results.cfm?mc='
	url_open(url)