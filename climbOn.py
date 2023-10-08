
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def scrapeClimbOn():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    res = []

    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    LINK = "https://climbonequipment.com/collections/climbing-shoes"
    SITE = "https://climbonequipment.com"


    currPage = 1
    lastPage = getLastPage(driver, LINK)

    while currPage <= lastPage:
        url = f'{LINK}?page={currPage}'
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        res.extend(scrapeCurrPage(soup, SITE))
        currPage += 1

    return res


def getLastPage(driver, LINK):
    """
    Get last page # 

    :param driver:
    :paramType driver:
    :param LINK: Url of first category page 
    :paramType LINK: String
    :return: last page 
    :returnType: int
    """

    driver.get(LINK)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    pageDiv = soup.find("div", {"class": "pagination"})
    pageNums = pageDiv.find_all("span", {"class":"page"})
    return int(pageNums[-1].text)

def scrapeCurrPage(soup, SITE):
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

        link = SITE + listing.find("a", {"class": "grid-product__link"})["href"]
        product = listing.find("div", {"class": "grid-product__title"}).text
        brand = listing.find("div", {"class": "grid-product__vendor"}).text
        priceDIV = listing.find("div", {"class": "grid-product__price"})
        origPrice = float(priceDIV.find("span",{"class":"grid-product__price--original"}).text.replace("$","").replace(" CAD", ""))
        salePrice = float(priceDIV.find_all("span",{"class":"visually-hidden"})[-1].next_sibling.replace("$","").replace("\n","").replace("from ",""))
        discountPct = round((origPrice - salePrice) / origPrice * 100)

        item = {
            "link": link,
            "product": product,
            "brand": brand,
            "origPrice": origPrice,
            "salePrice":salePrice,
            "discountPct":discountPct
        }
        products.append(item)
    return products


