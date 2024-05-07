
#Libraires required in the project
import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin


header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}


def get_response(url):
    response = httpx.get(url, headers=header)
    try:
        response.raise_for_status()
    except httpx.RequestError as exc:
        print(f"Error while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(f"Error response from the server: {exc}")
    except httpx.TimeoutException as exc:
        print(f"Request timed out: {exc}")
    else:
        print(f"Successfully made request to server")
    finally:
        print(f'Status code of respective page is {response.status_code}', end="\n\n")
        return response.text
    

def prase_page(response : HTMLParser):
    html = HTMLParser(response)
    return html


def select_products(html):
    """
        Select all the products that are listed on the page
    """
    products = html.css("li a.O8aFd2MOq4cf8b3yUR2p.tS6GbfEJ9cTyCftpIpEO")
    return products


def extract_text(selector):
    """
        extract the text from the css selector and returns text from it otherwise returns None
    """
    try:
        return selector.text()
    except AttributeError:
        return None


def next_page(html):
    """
        this function serach for next page link in current page
    """
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

    while True:
        products = select_products(html)        
        print("\nGathering product information on page", counter)
        for product in products:
            print(product.attributes.keys())
            print(urljoin("https://www.rei.com/c/mens-clothing/f/scd-deals", product.attributes['href']))
            product_resp = httpx.get(urljoin("https://www.rei.com/c/mens-clothing/f/scd-deals", product.attributes['href']), headers=header, follow_redirects=True)
            product_html = HTMLParser(product_resp.text)
            product_data = {
                "Brand" : extract_text(product.css_first("span[data-ui=product-brand]")),
                "Product Name" :extract_text(product.css_first("span[data-ui=product-title]")),
                "Sale Price" :extract_text(product_html.css_first("#buy-box-product-price")),
                "Full Price" :extract_text(product_html.css_first("#buy-box-product-price-compare")),
                "Rating" : extract_text(product_html.css_first("#product-rating > a > span.cdr-rating__count_15-0-0 > span.cdr-rating__number_15-0-0")),
                "Number of reviews": extract_text(product_html.css_first("#product-rating > a > span.cdr-rating__count_15-0-0 > span:nth-child(2)")),
                "Product url": urljoin("https://www.rei.com/c/mens-clothing/f/scd-deals", product.attributes['href'])
            }
            print(product_data)
        next_url = next_page(html)
        if next_url is None:
            break
        html = prase_page(get_response(next_url))
        time.sleep(2)
        counter += 1


if __name__ == "__main__":
    main()