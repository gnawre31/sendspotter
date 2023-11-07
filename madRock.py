from bs4 import BeautifulSoup
import requests

from Product import Retailer
from Product import Product





def scrapeMadRock():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Mad Rock Canada", country="Canada", currency="CAD")

    LINK = "https://www.madrock.ca/collections/rock-shoes"
    SITE = "https://www.madrock.ca"

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
    return len(pageNums)

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
    listings = soup.find_all("div", {"class": "grid__item"})
    for listing in listings:

        isDiscounted = listing.find("div", {"class": "product-tag"})
        if isDiscounted is None:
            continue
        
        product = Product()

        product.web_url = SITE + listing.find("a", {"class": "product-card"})["href"]
        product.scraped_product_name = listing.find("div", {"class": "product-card__name"}).text
        product.scraped_brand = "Mad Rock"

        # skip approach shoes
        if "approach" in product.scraped_product_name.lower():
            continue



        priceDIV = listing.find("div", {"class": "product-card__price"})

        product.og_price = float(priceDIV.find("s",{"class":"product-card__regular-price"}).text.replace("$",""))
        product.sale_price = float(priceDIV.text.replace(" ","").split('\n')[4].replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

        imgTag = listing.find("img", {"class":"product-card__image"})
        product.img_url = "https:" + imgTag['src']

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)

    return products
    


if __name__ == "__main__":
    res = scrapeMadRock()
    # res.printList()
    res.saveToSheets()



