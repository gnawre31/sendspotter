from bs4 import BeautifulSoup
import requests

from Product import Retailer
from Product import Product





def scrapeClimbOn():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Climb On Squamish", country="Canada", currency="CAD")

    LINK = "https://climbonequipment.com/collections/climbing-shoes"
    SITE = "https://climbonequipment.com"

    currPage = 1
    lastPage = getLastPage(LINK)


    while currPage <= lastPage:
        
        url = f'{LINK}?page={currPage}'
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, "html.parser")
        products = scrapeCurrPage(soup, SITE, retailer)
        retailer.addProducts(products)
        currPage += 1

    return retailer


def getLastPage(LINK):
    """
    Get last page # 

    :param driver:
    :paramType driver:
    :param LINK: Url of first category page 
    :paramType LINK: String
    :return: last page 
    :returnType: int
    """

    # driver.get(LINK)
    response = requests.get(LINK) 
    # print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    pageDiv = soup.find("div", {"class": "pagination"})
    pageNums = pageDiv.find_all("span", {"class":"page"})
    return int(pageNums[-1].text)

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
    listings = soup.find_all("div", {"class": "grid-product"})
    for listing in listings:

        isDiscounted = listing.find("div", {"class": "grid-product__tag--sale"})
        if isDiscounted is None:
            continue

        product = Product()

        product.web_url = SITE + listing.find("a", {"class": "grid-product__link"})["href"]
        product.scraped_product_name = listing.find("div", {"class": "grid-product__title"}).text
        product.scraped_brand = listing.find("div", {"class": "grid-product__vendor"}).text

        priceDIV = listing.find("div", {"class": "grid-product__price"})

        product.og_price = float(priceDIV.find("span",{"class":"grid-product__price--original"}).text.replace("$","").replace(" CAD", ""))
        product.sale_price = float(priceDIV.find_all("span",{"class":"visually-hidden"})[-1].next_sibling.replace("$","").replace("\n","").replace("from ",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    return products
    


if __name__ == "__main__":
    res = scrapeClimbOn()
    # res.printList()
    res.saveToSheets()



