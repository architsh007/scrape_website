My learning of web scraping was done using httpx and selectolax instead of requests and beautifulsoup because there are several benefits to utilizing those libraries, such as httpx supporting the latest HTML5 and selectolax working on CPython, which is much faster than beautifulsoup.


The following programs will scrape the product data for men's apparel offers from rei.com. 

view_product_details.py:            This python program will show all of the product details that are available on the scraping website.
The file scrape_product_details.py: This Python script will extract all the product information on the page, including the product's name, brand, sale price, full price, ratings, quantity of 
                                    reviews, and website link, into a JSON file.

** scrape_website: This directory contains all of the necessary libraries needed to run applications in a virtual environment in Python.
