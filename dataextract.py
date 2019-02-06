# Debug mode
#  Comment out line 100 then debug mode.
# Paramenter
#  c_inputfile
#  c_xpath

import requests
import csv
import lxml.html
import requests
import requests.exceptions
import pandas as pd
from urllib import parse
from urllib.parse import urlsplit
import json
from time import sleep

c_inputfile = 'url_list.csv'

c_xpath = "//article/div/blockquote/p"
# c_css = "article div blockquote p"


# c_outputfile = 'output.json'

def rtv_data(url):
    path = url.split('/')
    quote_type = path[-2]
    print("INFO: rtv_data(): Quote", quote_type)

    response = requests.get(url)

    print("INFO: rtv_data(): URL Response", response.status_code)
    if response.status_code == 404 :
      return {response.status_code}

    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    
    quotes = []
    for rtvx in root.xpath(c_xpath):
    # for rtvx in root.cssselect(c_css):
      # print("INFO: rtv_data(): ", rtvx.text_content())
      # quotes.append(rtvx.text_content())
      quote = rtvx.text_content()
      
      i = findnameindex(quote)
      
      quote_x = {}
      quote_x["quote"] = quote[:i+1].strip()
      quote_x["author"] = quote[i+1:].replace("Click to tweet", "").strip()
      quotes.append(quote_x)

    return quotes

def findnameindex(quote):
  print("INFO: findnameindex(): param - ", quote)
  doti = quote.find(".")
  
  if doti == -1 :
    doti = quote.rfind("?", 0, -1)
    return doti
  
  end_i = -1
  min_i = -1 * len(quote) -1
  
  while True:
    if end_i <= min_i:
      break
    i = quote.rfind(".", 0, end_i)
    if not quote[i-1].isupper():
      doti = i
      break
    else:
      end_i = i - 1

  # print("INFO: findnameindex(): quote  - ", quote[0:doti+1].strip())
  # print("INFO: findnameindex(): author - ", quote[doti+1:].strip())
  return doti

def main():

  df = pd.read_csv(c_inputfile)

  base_list = []
  for index, row in df.iterrows():
    cp = row['name']
    cu = row['url']
    print("INFO: main(): ", cp, "," + cu)

    extractdata = rtv_data(cu)
    base_list = extractdata
    # base_list.append(extractdata)
    print("INFO: main(): ", cp, " - completed")

    c_outputfile = cp + '.json'
    f = open(c_outputfile, 'w')
    json.dump(base_list, f)
    
    break
    sleep(5)

if __name__=='__main__':
  main()

