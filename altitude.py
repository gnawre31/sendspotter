
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product

def scrapeAltitude():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Altitude Sports", country="Canada", currency="CAD")

    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    LINK = "https://www.altitude-sports.com/collections/gear-climbing-climbing-shoes#?filter.on_sale=Yes"
    SITE = "https://www.altitude-sports.com"
    driver.get(LINK)
    time.sleep(25)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = scrapeCurrPage(soup,SITE, retailer)
    retailer.addProducts(products)
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
    listings = soup.find_all("div", {"class": "ss-product__info"})
    # all products are discounted on this page

    for listing in listings:

        product = Product()

        product.web_url = SITE + listing.find("a", {"class": "ss-product__info__manufacturer"})['href']
        product.scraped_brand = listing.find("a", {"class": "ss-product__info__manufacturer"}).text.strip()
        product.scraped_product_name = listing.find("h3", {"class": "ss-product__info__name"}).text.strip()
        product.sale_price = float(listing.find("span",{"class":"ss-product__price--special"}).text.replace("$","").replace("CAN ","").strip())
        product.og_price = float(listing.find("span",{"class":"ss-product__price--old"}).text.replace("$","").replace("CAN ","").strip())
        product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    return products

if __name__=="__main__":
    res = scrapeAltitude()
    res.saveToSheets()

    # print(res)
