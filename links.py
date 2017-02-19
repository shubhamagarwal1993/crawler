#!/usr/bin/env python

# Used to extract data from the html
from lxml import html
# Used to make http requests like GET, POST, PUT, DELETE
import requests
# To sleep between GET requests on the same website
import time

# main class for crawling on given url
class appCrawler:

    # constructor -> self,
    #                url to crawl on
    #                depth 0, only current page; depth 1, 1 url deep....
    def __init__(self, url, depth):
        self.url = url
        # how many links / how deep we want to go
        self.depth = depth
        # current depth of crawler
        self.current_depth = 0 
        # list of all the links that we find at different depths
            # self.depth_links[0] - all links at depth 0
            # self.depth_links[1] - all links at depth 1
        self.depth_links = []
        # links that are retuned at current link
        self.apps = []

    # main entry point to crawling logic
    def crawl(self):
        # crawl first page by calling get_data_from_link function
        app = self.get_data_from_link(self.url)
        # print links at current depth
        self.apps.append(app)
        # save links at current depth with current depth id
        self.depth_links.append(app.links)

        # we are done crawling current depth
        # Start crawling next depth
        while self.current_depth < self.depth:
            # keep track of all links on current page
            current_links = []
            # We will crawl on all links of current deoth to crawl on next depth
            for link in self.depth_links[self.current_depth]:
                current_app = self.get_data_from_link(link)
                # append will add the list and make current links a list of lists
                # extend will add the data/links instead of adding a list
                # current list will thus have all links in one list
                current_links.extend(current_app.links)
                #add this new current_list to our data
                self.apps.append(current_app)
                # We will sleep for some time so that we dont make too many GET requests at once
                # This should prevent our ip from getting black listed
                time.sleep(5)
            # We are done with current depth, so go to next depth
            # Increment depth to keep of current depth
            self.current_depth += 1
            # add all links from current links to main list
            self.depth_links.append(current_links)


    # get data from one of the link that is passed to it.
    # This acts as a unit function which will be called on each link for which we want data
    def get_data_from_link(self, link):
        # get html for following page
        start_page = requests.get(link)

        # test the html data we get back
        # print start_page.text

        # take all the html in start_page and create a document tree out of it
        tree = html.fromstring(start_page.text)

        # use this tree to execute xpath queries and pull data out
        # to start from root use '//'
        filing = tree.xpath('//td[@nowrap="nowrap"]/text()')[0]
        # print filing
        links = tree.xpath('//table[@class="tableFile2"]/tr/td[@nowrap="nowrap"]/a/@href')[0]
        # print link

        # We can get all the data from the current page

        # Print the data by calling the print function defined below
        app = App(filing, link)

        #return app to crawl so we can store it there instead
        #self.apps.append(app)
        return app

# This class is the exact data we want for this app
class App:

    # constructor -> self,
    #                filing will be 13F*
    #                link will be the link to the document
    #                filing date is to get the quarter
    # All this is on the EDGAR website, we will get more data later
    def __init__(self, filing, links):
        self.filing = filing
        self.links = links

    # we will call this everytime to print or to put data in a file
    def __str__(self):
        return ("filing: " + self.filing.encode('UTF-8') +
                "\r\nlinks: " + self.links.encode('UTF-8') +
                "\r\n")

# create an instance of the crawler
# give it the first url to go to
# depth is 0 to get data of current page only
crawler = appCrawler('https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001166559&owner=exclude&action=getcompany&Find=Search', 0)

# use crawl function to start crawling on the given link
crawler.crawl();

# print the apps we get
for app in crawler.apps:
    print app

# def main():

# if __name__ == '__main__':
#     main()