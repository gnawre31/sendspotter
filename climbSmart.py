from bs4 import BeautifulSoup
import requests

from Product import Retailer
from Product import Product


from consts import BRANDS


def scrapeClimbSmart():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Climb Smart Shop", country="Canada", currency="CAD")

    LINK = "https://climbsmartshop.com/collections/clearance-shoes"
    SITE = "https://climbsmartshop.com"
        
    url = LINK
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, "html.parser")
    products = scrapeCurrPage(soup, SITE, retailer)
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
    listings = soup.find_all("a", {"class": "product-card"})
    for listing in listings:

        product = Product()

        product.web_url = SITE + listing['href']
        product.scraped_product_name = listing.find("div", {"class": "product-card__name"}).text
        product.scraped_brand = listing.find("div", {"class": "product-card__brand"}).text

        # skip if random item or if approach shoe
        if product.scraped_brand not in BRANDS or "approach" in product.scraped_product_name.lower():
            continue


        priceDIV = listing.find("div", {"class": "product-card__price"})

        product.og_price = float(priceDIV.find("s",{"class":"product-card__regular-price"}).text.replace("$","").replace(" CAD", ""))
        product.sale_price = float(priceDIV.text.split("\n")[4].strip().replace("$","").replace("\n","").replace("from ",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

        imgDiv = listing.find("div", {"class":"product-card__image-container"})
        product.img_url = "https:"+imgDiv.find("img")['data-src'].replace("width","720").replace("{","").replace("}","")

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)

    return products
    


if __name__ == "__main__":
    res = scrapeClimbSmart()
    # res.printList()
    res.saveToSheets()



