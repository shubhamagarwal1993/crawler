To run the program

python shubhamagarwal.py

OR

python shubhamagarwal.py <ticker>


Requirements:
sys
time
lxml (pip install)
requests (pip install)
mechanize (pip install)
python 2.7

Few things on what the program does:
- Takes a ticker
- validates it
Depth 1
- Enters the ticker and goes to the page
Depth 2
- Filters by 13F
- gets all document links from the page
Depth 3
- Goes to the document links and searches for the related 13F document on the page
Depth 4
- Gets 13f documents and appends them to a file

How to deal with different formats
- I think the most important thing is pre-defined headers in the file to read the value of and type of file (csv, xml, txt, etc.)

- Pick up any link/file which is on the page.
	- In our case, there are many formats of a single 13F file on the same page
- Then run the file name (with type) over an if elif else condition and send them to different file formatting parsers
- Each file formatting parser reads the file; picks up predefined field and value and adds it to a main file
- All parsers use the same format to append the data to the main file (like tab-delimited in our case)

* I did not get time to put much work on the file parsing, so i wrote something specific to this website in the format it is.
Also, I am not sure on how to read 13F files and did not try to grab fields from it.


Shubham Agarwal
shubhamagarwal1993@gmail.com
https://shubham.io