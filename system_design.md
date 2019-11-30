## Description:
 - Design a basic web-crawler, and web-scraper
 - Scrap on twitter with posts mentioning an input word, finding most meaningful tweet

### Requirements:
#### Creation, and User Account:
 - User needs to specify a URL, and any associated login
 - User can specify a tag and a series of associated words.
   - E.g. tag: description, words: [football, rams, score, final]
 - User can specify the max number of results to store, or 0 for all results.

#### Retrieval:
 - On using the tag and associated words, the scraper will find the most relevant information.
 - The top 20 most popular searches are stored by default.

#### Analytics:
 - Save search queries for user for analytics

#### Capacity:
 - Write heavy system
 - Check for memory limits before saving data

### Memory Management and Capacity calculations:
 - On an avg, a website has 100 links on it. Let's considering a n-ary tree, where n = 100.
 - Assume a restriction to stop searching beyond 2 levels deep
 - Only provide top 5000 results by default

#### Traffic calculations:
 - Let's assume each website has 100 external links, and we only search 2 levels deep
 - Total links to search, with no overlapping links: n^0 + n^1 + n^2 => 1 + 100 + (100^100)
 - Assume 20% hit, total websites to get a score for
   - (20/100) * (101 + 100^100) => 2 * (10^199)

 - Assume 5 url's can be processed per second by each computer process for a score, and whether it should be saved or not

#### Database memory calculations
 - Assume average size of each web page is 
   words on each page => 1000
   Each byte can store 1 character. A tinyURL, full URL, and other details should be about 500 to 1000 characters. That would be 1 Kilobyte (1000 Byte)
   character in each word => 5, total characters => 5000 => total space for each page 5000 bytes => total space for each page => 5 kb.

 - You should know this:
   ASCII ranges from 0 to 127, and needs 1 byte to store a character.
   Utf-8 ranges from 1 byte to 6 bytes depending on the character.

 - Total memory => total pages * page per size => 5000 * 5 kb => 25000 kb => 25 Mb

#### Caching, and backlinks memory calculations
 - Caching will be used to find pages already visited.
 - The web has around 200 million active websites.
 - Max url length => 2048 characters => conservative max average for url length => 1000 characters
   - Size needed for each url -> 1000 characters -> 1000 bytes -> 1kb
   - Size needed to keep score of each url -> 4 bytes
 - Total size for 200 million urls -> 200 million * 1004 bytes -> 200,800,000,000 bytes -> 200,800 Mb -> 201 Gb

 - Keep all urls pointing to a url, so as to calculate backlinks
 - Assuming each website points to each website -> 200 * 200 Gb -> 40000 Gb -> 40Tb
   In general, each link has about 50 backlinks -> (51 * 200 million) * 1000 bytes -> 10,200,000,000 * 1000 bytes
   -> 10,200,000 Mb -> 10,200 Gb -> 11 Tb

#### Bandwidth calculations
 - Assuming we have the capacity to process 200 urls/sec; previous using 5 per second from a single process
 - For incoming data:
   (URLs processed / second) * (size of each URL + size of URL data blob)
   (200 URLs / sec) * (1Kb + 5KB)
   200 * 6 Kb / sec
   1200KB / sec => 1.2 Mb/sec

 - For outgoing data:
   (URLs processed / second) * (size of each URL)
   (200 URLs / sec) * 1Kb
   200 Kb/sec

### API design
 - Use REST API endpoints so other services can use it.
   Get:
   getSearchResults(loginToken, URL=None, searchQuery=None, strict=None):
   loginToken: The user token to track for analytics, throttle max usage, or detect spamming
   URL: The url to start the search at, if none provided, then some default urls will be used, like google.com
   searchQuery: The tags and associated words, if none provided, then latest urls like news, sports and weather provided.
      [
          <tag name>: [<word1>, <word2>, ...],
          <tag name>: [<word1>, <word2>, ...],
          <tag name>: [<word1>, <word2>, ...],
      ]
   strict: Boolean, if words to be strict checked or substring matched with some edit distance.

   Return val: list of search results

### Database design
 - Caching, and score database
   Redis key-value store, where key is a string type, and value is an integer type

 - Backlink database
   Redis key-value store, where key is a string type, and value is a list of strings

 - User account
   If we are keeping tab on who made the query, then maintain a sql database
   Columns should be unique id, first, last, email, created datetime

 - Query database
   Sql table with columns as unique id, foreign key user id, url, created datetime

 - Tags database
   Redis table with key as query id, and value as list of key-value pair where key is tag name, and value is list of associated words.

### Algorithm
 - Take URL, check for it's existence in cache to not crawl it again, get data from page.
 - Search page:
   - Update backlink database
   - Update score, and visited database
 - Add all urls in page to a queue, so as to do a BFS
