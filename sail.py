
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product

def scrapeSail():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Sail", country="Canada", currency="CAD")

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    LINK = "https://www.sail.ca/en/outdoor-gear/climbing/climbing-shoes#/filter:ss_special_price:Yes"
    driver.get(LINK)
    time.sleep(25)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = scrapeCurrPage(soup, retailer)
    retailer.addProducts(products)
    return retailer





def scrapeCurrPage(soup, retailer):
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
    listings = soup.find_all("li", {"class": "product-item"})
    # all products are discounted on this page

    for listing in listings:

        product = Product()

        product.web_url =  "https:" + listing.find("a", {"class": "product-item-link"})['href']

        productDIV = listing.find_all("div",{"class":"sub-content-wrapper"})[0]
        priceDIV = listing.find_all("div",{"class":"sub-content-wrapper"})[1]

        product.scraped_brand = productDIV.find("div", {"class": "product-item-manufacturer"}).text
        product.scraped_product_name = productDIV.find("span", {"class": "product-item-name"}).text
        product.sale_price = float(priceDIV.find_all("span",{"class":"price-container"})[0].text.replace("$",""))
        product.og_price = float(priceDIV.find_all("span",{"class":"price-container"})[1].text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)


        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    return products

if __name__=="__main__":
    res = scrapeSail()
    res.saveToSheets()

    # print(res)
