#!/usr/bin/env python

import re, urllib
import requests
from lxml import html

def main():

    # Enter ticket and go to web page

    # url = 'https://www.sec.gov/edgar/searchedgar/companysearch.html'

    # payload = {
    #    "CIK": "0001166559"
    # }

    # session_requests = requests.session()
    # #result = session_requests.get(url)
    # #tree = html.fromstring(result.text)

    # result = session_requests.post(
    #     url,
    #     data = payload, 
    #     headers = dict(referer=url)
    # )

    # #get new url as page redirects
    # url = result.url
    # print result
    # print url

    # Get all HTML on the page
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001166559&owner=exclude&action=getcompany&Find=Search"
    handle = urllib.urlopen(url)

    html_gunk =  handle.read()

    #parse all 
    file = open('depth_1.txt', 'w')
    file.write(html_gunk)
    file.close()

    #parse html as a tree so we can get all 13F documents
    


if __name__ == '__main__':
    main()