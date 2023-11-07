
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product

def scrapeVPO():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="VPO", country="Canada", currency="CAD")

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    LINK = "https://vpo.ca/category/181/shoes"
    SITE = "https://vpo.ca"

    currPage = 1
    lastPage = 1

    

    while currPage <= lastPage:
        url = f'{LINK}?pagenum={currPage}'
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        if currPage == 1:
            pages = soup.find_all("li",{"class":"ss-page"})
            lastPage = len(pages)-1
        
        products = scrapeCurrPage(soup, SITE, retailer)
        retailer.addProducts(products)
        currPage+= 1

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
    listings = soup.find_all("div", {"class": "productBox"})

    for listing in listings:
        isDiscounted = listing.find("span", {"class": "ss-badge-main-text"})
        if isDiscounted is None:
            continue
        elif "New" in isDiscounted.text:
            continue


        product = Product()

        product.web_url =  SITE + listing.find("a", {"class": "productLinks"})['href']

    #     productDIV = listing.find_all("div",{"class":"sub-content-wrapper"})[0]
        priceDIV = listing.find_all("span",{"class":"ss-sale-price"})

        product.scraped_brand = listing.find("h5", {"class": "brand"}).text
        product.scraped_product_name = listing.find("div", {"class": "productTitle"}).text
        product.sale_price = float(priceDIV[0].text.replace("$",""))
        product.og_price = float(priceDIV[-1].text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)

        imgDiv = listing.find("div",{"class":"mediumImg"})
        product.img_url = "https:" + imgDiv.find("img")['src']


        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    return products

if __name__=="__main__":
    res = scrapeVPO()
    res.saveToSheets()

    # print(res)
