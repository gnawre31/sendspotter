
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product
from consts import BRANDS

def scrapeMonodSports():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Monod Sports", country="Canada", currency="CAD")

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    LINK = "https://www.monodsports.com/collections/rock-shoes?sort_by=best-selling&filter.p.m.custom.on_sale=Yes"
    SITE = "https://www.monodsports.com"
    driver.get(LINK)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = scrapeCurrPage(soup, SITE, retailer)
    retailer.addProducts(products)
    return retailer



def getBrandLenFromStr(product_title):
    product_title = product_title.lower()


    matched = ""
    for b in BRANDS:
        if b.lower() in product_title:
            matched = b
            break

    return len(matched)


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
    listings = soup.find_all("div", {"class": "product-grid-item"})

    # all products are discounted on this page

    for listing in listings:

        product = Product()

        product.web_url =  SITE + listing.find("a", {"class": "product__media__holder"})['href']

        product_title = listing.find("a",{"class":"product-grid-item__title"}).text
        brandLen = getBrandLenFromStr(product_title)
        product.scraped_product_name = product_title[brandLen:].strip().replace("(Past Season)","")
        product.scraped_brand = product_title[0:brandLen]

        priceDIV = listing.find("a",{"class":"product-grid-item__price"})
        
        product.sale_price = float(priceDIV.find("span",{"class":"product-grid-item__price__new"}).text.replace("$",""))
        product.og_price = float(priceDIV.find("s").text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)

        product.img_url = "https:" + listing.find("picture").find("source")['data-srcset'].split(', ')[-1].split(" ")[0]

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)

    return products

if __name__=="__main__":
    res = scrapeMonodSports()
    # res.printList()
    res.saveToSheets()

    # print(res)
