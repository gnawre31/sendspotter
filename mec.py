
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product

from consts import BRANDS





def scrapeMEC():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    



    retailer = Retailer(retailer="MEC", country="Canada", currency="CAD")

    LINK = "https://www.mec.ca/en/products/climbing/climbing-footwear/rock-climbing-shoes/c/1190?filters%5Bcustom_fields.badge%5D%5B0%5D=clearance"
    SITE = "https://www.mec.ca"

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

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
        if b in product_title:
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
    listings = soup.find_all("div", {"class": "findify-components--cards--product"})

    for listing in listings:

        product = Product()

        product.web_url = SITE + listing.find("a", {"class": "findify-components--cards--product__rating"})["href"]
        product_title = listing.find("h3",{"class":"findify-components--cards--product__title"}).text

        brandLen = getBrandLenFromStr(product_title)
        product.scraped_product_name = product_title[brandLen:].strip()
        product.scraped_brand = product_title[0:brandLen]


        product.og_price = float(listing.find("span",{"class":"findify-components--cards--product--price__compare"}).text.replace("$","").replace(" CAD", ""))
        product.sale_price = float(listing.find("span",{"class":"findify-components--cards--product--price__sale-price"}).text.replace("$","").replace("\n","").replace("from ",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

        imgDiv = listing.find("div", {"class":"findify-components-common--image"})
        # print(imgDiv)
        product.img_url = imgDiv.find("img")['src']



        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    return products
    


if __name__ == "__main__":
    res = scrapeMEC()

    res.saveToSheets()


    


