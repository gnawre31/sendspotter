import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from Product import Retailer
from Product import Product



LINK = "https://shop.blocshop.com/collections/all-climbing-shoes"
SITE = "https://shop.blocshop.com"


def open_chrome_browser_function(LINK):
    """Opens Google Chrome browser via Selenium"""
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(ChromeDriverManager.install(), options=options)
    driver.get(LINK)
    
    return driver

def scrapeClimbOn():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """
    #open the chrome browser
    global LINK
    global SITE
    driver = open_chrome_browser_function(LINK)
    time.sleep(2) #1 seconds to allow page to load

    retailer = Retailer(retailer="Bloc Shop", country="Canada", currency="CAD")
    retailer.validate()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    #test to be removed 
    sale_spans = soup.find_all('span', {"class": "sale"})
    print ('sale scraping number of products went wrong ') if len(sale_spans) != len(products) else print('number of sale items match number of scraped sale items')
        

    #parse page html
    products = scrapeCurrPage(soup, SITE, retailer)
    
    #test 
    print(f"{retailer.retailer} in {retailer.country} has {retailer.products}")
    
    return retailer


def scrapeCurrPage(soup, SITE, retailer):
    """
    Get product details for all discounted products on a single page
    
    :param soup: Parsed HTML for current product page 
    :paramType:
    :param SITE: Root domain, used to links to product detail pages (PDP)
    :paramType: String
    :return: list of details for discounted products on current page
    :returnType: List
    """
    products = []
    listings = soup.find("div", {"class": "collection__grid grid"}).contents
    for listing in listings:

        isDiscounted = listing.find("span", {"class": "sale"})
        if isDiscounted is None:
            continue

        product = Product()
        
        product.web_url = SITE + listing.find("a", {"class": "product-item__image-link borders"})["href"]
        product.scraped_brand = listing.find("a", {"class": "product-item__image-link borders"})["title"]
        product.scraped_product_name = listing.find("a", {"class": "product-item__image-link borders"})["title"]
        
        product.og_price = float(listing.find("s",{"class":"t-subdued"}).text.replace("$","").replace(" CAD", ""))
        product.sale_price = float(listing.find("span",{"class":"sale"}).text.replace("$","").replace("\n",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)
        
        if product.validate() is False:
            print(product)
            continue

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)
        products.append(product)
    
    #close the driver
    driver.quit()
    
    return products


if __name__ == "__main__":
    res = scrapeClimbOn()
    print(res)
    # res.saveToSheets()
    
    # res.printList()
    # print(res)
    # retailer = Retailer("MEC")


