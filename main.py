import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin


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
        return selector.text()
    except AttributeError:
        return None


def extract_full_price(product):
    if extract_text(product.css_first("span[data-ui=full-price]")) is not None:
        return extract_text(product.css_first("span[data-ui=full-price]"))
    else:
        return extract_text(product.css_first("span[data-ui=compare-at-price]"))


def product_details(product):
    """
        extract deatils of the products from the results and prints the result
    """
    item = {
        "Brand" : extract_text(product.css_first("span[data-ui=product-brand]")),
        "Name of product" : extract_text(product.css_first("span[data-ui=product-title]")),
        "Sale price" : extract_text(product.css_first("span[data-ui=sale-price]")),
        "Full price" : extract_full_price(product)
    }
    return item


def next_page(html):
    if html.css_first("a[data-id=pagination-test-link-next]") == None:
        print("This is the last page")
        exit()
    else:
        time.sleep(2)
        return urljoin("https://www.rei.com/c/mens-clothing/f/scd-deals", html.css_first("a[data-id=pagination-test-link-next]").attributes["href"]) 


def main():
    base_url = "https://www.rei.com"
    url_to_scrape = "https://www.rei.com/c/mens-clothing/f/scd-deals"
    
    html = prase_page(get_response(url_to_scrape))
    next_url = next_page(html)
    counter = 1

    while next_url is not None:
        next_url = next_page(html)
        products = select_products(html)        
        print("\nGathering product information on page", counter)    
        for product in products:
            print(product_details(product))
        html = prase_page(get_response(next_url))
        counter += 1
    

if __name__ == "__main__":
    main()

