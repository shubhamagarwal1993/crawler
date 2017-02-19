#!/usr/bin/env python
import sys
# Used to extract data from the html
from lxml import html
# To sleep between GET requests on the same website
import time
import requests
# To fill form (ticket) and click on search button
import mechanize
from mechanize import Browser
# To parse xml files
from xml.sax.handler import ContentHandler
import xml.sax


# main class for crawling on given url
class appCrawler:
    def __init__(self, url, CIK, depth, links, link_13F_xml, link_13F_txt):
        # starting website url
        self.url = url
        # ticker value
        self.CIK = CIK
        # how many links / how deep we want to go
        self.depth = depth
        # maintain all links for 13F pages in this list
        self.links = []
        # keep all 13F xml files here
        self.link_13F_xml = link_13F_xml
        # keep all 13F txt files here
        self.link_13F_txt = link_13F_txt

    # main entry point to crawling logic
    def crawl(self):

        # initiating a browser
        br = mechanize.Browser()
        # ignore robots.txt
        br.set_handle_robots(False)
        # our identity
        br.addheaders = [("User-agent","Mozilla/5.0")]
        # requesting the github base url
        try:
            gitbot = br.open(self.url)
        except (mechanize.HTTPError,mechanize.URLError) as e:
            if isinstance(e,mechanize.HTTPError):
                print e.code
            else:
                print e.reason.args
            return

        # the CIK form has 3 other forms before it
        br.select_form(nr=4)
        # CIK value
        br["CIK"] = self.CIK
        # click the search button
        response = br.submit()

        #print response.read()
        self.url = response.geturl()

        # crawl page with CIK to get all 13F reports on the page
        # link is a list with all 13F report links
        links = self.get_data_from_link(self.url, self.links)


        return links

    # get data from one of the link that is passed to it.
    # This acts as a unit function which will be called on each link for which we want data
    def get_data_from_link(self, url, links):

        # initiating a browser
        br = mechanize.Browser()
        # ignore robots.txt
        br.set_handle_robots(False)
        # our identity
        br.addheaders = [("User-agent","Mozilla/5.0")]
        # requesting the github base url
        gitbot = br.open(self.url)

        # Check if ticker is valid
        try:
            br.select_form(nr=0)
        except Exception:
            print "ticket not valid"
            return

        # the CIK form has 3 other forms before it
        br.select_form(nr=0)

        br["type"] = "13F"
        # click the search button
        # response has all the html
        response = br.submit()
        #print response.read()

        # take all the html in start_page and create a document tree out of it
        tree = html.fromstring(response.read())

        # use this tree to execute xpath queries and pull data out
        # to start from root use '//'
#        current_page_links = tree.xpath('//table[@class="tableFile2"]/tr/td[@nowrap="nowrap"]/a/@href')
        #get all links from the 2nd column of the table
        current_page_links = tree.xpath('//table[@class="tableFile2"]/tr/td[2]/a/@href')

        for index, link in enumerate(current_page_links):
            link = "https://www.sec.gov/" + link
            self.links.append(link)

        return

class store_file:
    def __init__(self, url):
        # starting website url
        self.url = url

    # main entry point to crawling logic
    def find_file(self, crawler):

        current_page = requests.get(self.url)
        tree = html.fromstring(current_page.text)
        link = tree.xpath('//table[@class="tableFile"]/tr/td/a/@href')
        if len(link) == 2:
            curr_link = "https://www.sec.gov/" + link[0]
            crawler.link_13F_txt.append(curr_link)
        elif len(link) == 5:
            curr_link = "https://www.sec.gov/" + link[1]
            crawler.link_13F_xml.append(curr_link)

class textHandler(ContentHandler):
    def characters(self, ch):
        sys.stdout.write(ch.encode("Latin-1"))

def main():
    
    # Get CIK
    if len(sys.argv) > 1:
        # CIK is argument
        CIK = sys.argv[1]
    else:
        # Get CIK from user
        CIK = raw_input("Enter ticker of CIK: ")

    # make object
    print 'entering ticker'
    crawler = appCrawler('http://www.sec.gov/edgar/searchedgar/companysearch.html', CIK, 0, [], [], [])
    print 'searching ticker page'
    # crawl on given link and 
    crawler.crawl();
    print 'got list of 13F files'

    # Go through each link and get 13F form from each link
    # Parse each form
    # store in file
    print 'storing 13F files'
    i = 0
    for link in crawler.links:
        file_13F = store_file(link)
        file_13F.find_file(crawler);

    print 'writing all 13F files to files13F.txt'
    # Store all 13F files in one file
    f = open("files13F.txt", "w")
    # txt files do not need to be changed
    i = 0
    for file in crawler.link_13F_txt:
        f.write("\n\n\nFile no: %d\n" % i)
        f.write("=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n\n\n")
        curr_file_content = requests.get(file)
        f.write(curr_file_content.text)
        i = i + 1
    # xml files are converted to txt and then stored
    for file in crawler.link_13F_xml:
        f.write("\n\n\nFile no: %d\n" % i)
        f.write("=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n\n\n")
        # curr_file_content = requests.get(file)
        # tree = ET.parse(curr_file_content.text)
        # print(ET.tostring(tree, encoding='utf-8', method='text'))
        curr_file_content = requests.get(file)
        f.write(curr_file_content.text)
        i = i + 1
    f.close()
    print 'done'

# Start
if __name__ == '__main__':
    main()

# Testing variables
    #CIK = '0001166559'