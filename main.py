import httpx
from selectolax.parser import HTMLParser
import time


def get_response(url):
    """
        This functions get repsonse from the given url outputs wheather site accessible or not by following code of status 
    """

    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    response = httpx.get(url, headers=headers, follow_redirects=True)
    
    if int(response.status_code) == 200:
        print("\nGot the successful response from website, with given code",response.status_code, end="\n\n")
    else:
        print(f"Got the following error while getting reposne from the site: {response.status_code}", end="\n\n")

    return response


def prase_page(response):
    """
        prase the response form the website
    """
    html = HTMLParser(response.text)
    return html


def select_products(html):
    """
        Select all the products that are listed on the page
    """
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    return products


def extract_text(selector):
    """
        extract the text from the css selector and returns text from it otherwise returns None
    """
    try:
        return selector
    except AttributeError:
        return None


def product_details(product):
    """
        extract deatils of the products from the results and prints the result
    """
    item = {
        "Brand" : extract_text(product.css_first("span[data-ui=product-brand]").text()),
        "Name of product" : extract_text(product.css_first("span[data-ui=product-title]").text()),
        "Sale price" : extract_text(product.css_first("span[data-ui=sale-price]").text()),
        "Full price" : extract_text(product.css_first("span[data-ui=full-price]").text())
    }
    return item


def main():
    base_url = "https://www.rei.com"
    url_to_scrape = "https://www.rei.com/c/mens-clothing/f/scd-deals"
    
    html = prase_page(get_response(url_to_scrape))
    
    products = select_products(html)
    
    for product in products:
        print(extract_text(product_details(product)))


if __name__ == "__main__":
    main()

