# 01 : preliminary version
# 02 : ok, todo - url nesting, ignore ? and #
# 03 : ok - completd print, level, filter - todo resource, level
import requests
import csv
import lxml.html
from urllib import parse
from urllib.parse import urlsplit
from collections import deque
import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions

# Example
#   c_targeturl = "http://ccows.csumb.edu/wiki/index.php/List_of_Environmental_Consultants_working_in_the_California_Central_Coast_Region"
#   c_css = '#mw-content-text > table > tr > th > a'

c_targeturl = "http://wisdomquotes.com/"
c_css = "#post-156 > div > p > a"

c_outputfile = 'url_list.csv'

def main():

  response = requests.get(c_targeturl)
  root = lxml.html.fromstring(response.content)
  root.make_links_absolute(response.url)

  with open(c_outputfile, 'w', newline='', encoding="utf-8") as csvf:
    writer = csv.writer(csvf, lineterminator='\n')
    writer.writerow(["name", "url"])
    for a in root.cssselect(c_css):
      print("INFO: main(): ", a.text, "," + a.get('href'))
      base_list = [a.text, a.get('href')]
      writer.writerow(base_list)
      #break

if __name__=='__main__':
  main()

