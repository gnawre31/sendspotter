from bs4 import BeautifulSoup
import requests

from Product import Retailer
from Product import Product


from consts import BRANDS


def scrapeMomoSports():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Momo Sports", country="Canada", currency="CAD")

    LINK = "https://momosports.ca/en/sports-et-activites/escalade/chaussons-d-escalade?am_on_sale=1&product_list_limit=36"
    SITE = "https://momosports.ca"


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
    listingsDIV = soup.find("ol",{"class":"products"})
    listings = listingsDIV.find_all("li", {"class": "product-item"})
    for listing in listings:

        product = Product()

        product.web_url = listing.find("a",{"class":"product-item-photo"})['href']
        product.scraped_product_name = listing.find("a", {"class": "product-item-link"}).text.strip()
        product.scraped_brand = listing.find("div", {"class": "product-brand"}).text.strip()

        priceDIV = listing.find_all("span", {"class": "price"})

        product.og_price = float(priceDIV[1].text.replace("$",""))
        product.sale_price = float(priceDIV[0].text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

        product.img_url = listing.find("img", {"class":"product-image-photo"})['src']

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)


    return products
    


if __name__ == "__main__":
    res = scrapeMomoSports()
    # res.printList()
    res.saveToSheets()



