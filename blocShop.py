
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product

def scrapeBlocShop():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    links = {
        "la sportiva":"https://shop.blocshop.com/collections/la-sportiva/shoes",
        "scarpa":"https://shop.blocshop.com/collections/scarpa-1/shoes",
        "tenaya": "https://shop.blocshop.com/collections/tenaya/shoes",
        "unparallel":"https://shop.blocshop.com/collections/unparallel",
        "five ten":"https://shop.blocshop.com/collections/five-ten/shoes",
        "evolv":"https://shop.blocshop.com/collections/evolv/shoes",
        "mad rock":"https://shop.blocshop.com/collections/mad-rock/shoes",
        "black diamond":"https://shop.blocshop.com/collections/black-diamond-shoes"
    }

    
    
    retailer = Retailer(retailer="Bloc Shop", country="Canada", currency="CAD")

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    SITE = "https://shop.blocshop.com"

    for brand in links.keys():
        LINK = links[brand]
        driver.get(LINK)
        time.sleep(2)

        # scroll down once
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = scrapeCurrPage(soup, SITE, retailer, brand)
        retailer.addProducts(products)
    return retailer





def scrapeCurrPage(soup, SITE, retailer, brand):
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
    listings = soup.find_all("div", {"class": "grid__item"})

    for listing in listings:


        isDiscounted = listing.find("div", {"class": "product-item__badge--sale"})
        if isDiscounted is None:
            continue

        

        product = Product()

        product.web_url =  SITE + listing.find("a", {"class": "product-item__image-link"})['href']


        productDIV = listing.find("div",{"class":"product-item"})


        product.scraped_brand = brand
        product.scraped_product_name = productDIV.find("h4").text

        sale_price_text = productDIV.find("span",{"class":"sale"}).text
        sale_price = sale_price_text.split("\n")[0]
        

        product.sale_price = float(sale_price.replace("$",""))
        product.og_price = float(productDIV.find("s",{"class":"t-subdued"}).text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)

        # imgDiv = productDIV.find("div",{"class":"image"})
        product.img_url = "https:" + productDIV.find("img", {"class":"image__img"})['src']


        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    return products

if __name__=="__main__":
    res = scrapeBlocShop()

    res.saveToSheets()

    # print(res)
