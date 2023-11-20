from bs4 import BeautifulSoup
import requests

from Product import Retailer
from Product import Product





def scrapeWalnuts():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Walnuts Climbing", country="Canada", currency="CAD")

    LINK = "https://wallnuts.store/collections/climbing-shoes?page=1"
    SITE = "https://wallnuts.store"
    
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
    listings = soup.find_all("div", {"class": "product-item-block"})

    for listing in listings:

        isDiscounted = listing.find("span", {"class": "product-label--on-sale"})
        if isDiscounted is None:
            continue

        product = Product()

        product.web_url = SITE + listing.find("a", {"class": "product-card__link-title"})["href"]
        product.scraped_product_name = listing.find("span", {"class": "product-card__title"}).text
        product.scraped_brand = listing.find("a", {"class": "product-item__vendor"}).text


        priceDIV = listing.find("div", {"class": "product-item__price_and_reviews_row"})

        product.og_price = float(priceDIV.find("s",{"class":"price-item--regular"}).text.replace("$",""))
        product.sale_price = float(priceDIV.find("span",{"class":"price-item--sale"}).text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

        product.img_url = "https:" + listing.find("img", {"class":"product-card__image"})['src']

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)

    return products
    


if __name__ == "__main__":
    res = scrapeWalnuts()

    res.saveToSheets()



