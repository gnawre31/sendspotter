
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import time
from Product import Retailer
from Product import Product

from consts import BRANDS

def scrapeLaCordee():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="La Cordee", country="Canada", currency="CAD")

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    LINK = "https://www.lacordee.com/en/climbing/climbing-shoes/climbing-shoes?page=1&on_sale_status%5Bfilter%5D=On+sale%2C1"
    SITE = "https://www.lacordee.com"
    driver.get(LINK)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = scrapeCurrPage(soup, SITE, retailer)
    # retailer.addProducts(products)
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
    listings = soup.find_all("article", {"class": "item-root-Fmc"})
    # all products are discounted on this page

    for listing in listings:

        product = Product()

        product.web_url =  SITE + listing.find("a", {"class": "item-images-KDW"})['href']

        productText = listing.find("a",{"class":"item-name-YL8"}).text

        # skip approach shoes
        if "approach" in productText.lower() or "leather" in productText.lower() or "tx2" in productText.lower() or "hiking" in productText.lower():
            continue

        brandLen = getBrandLenFromStr(productText)
        product.scraped_product_name = productText[brandLen:].strip()
        product.scraped_brand = productText[0:brandLen]
        # priceDIV = listing.find_all("div",{"class":"sub-content-wrapper"})[1]

        # product.scraped_brand = productDIV.find("div", {"class": "product-item-manufacturer"}).text
        # product.scraped_product_name = productDIV.find("span", {"class": "product-item-name"}).text
        # product.sale_price = float(priceDIV.find_all("span",{"class":"price-container"})[0].text.replace("$",""))
        # product.og_price = float(priceDIV.find_all("span",{"class":"price-container"})[1].text.replace("$",""))
        # product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)

        # imgDiv = listing.find("span",{"class":"product-image-wrapper"})
        # product.img_url = imgDiv.find("img")['src']


        # product.getGender()
        # product.getMatchedBrand()
        # product.getMatchedProduct()
        # product.generateID(retailer)
        # product.printProduct()

        product.printProduct()

        products.append(product)
    return products

if __name__=="__main__":
    res = scrapeLaCordee()
    res.printList()
    # res.saveToSheets()

    # print(res)






https://www.lacordee.com/graphql?query=query+GetCategories%28%24id%3AString%21%24pageSize%3AInt%21%24currentPage%3AInt%21%24filters%3AProductAttributeFilterInput%21%24sort%3AProductAttributeSortInput%29%7Bcategories%28filters%3A%7Bcategory_uid%3A%7Bin%3A%5B%24id%5D%7D%7D%29%7Bitems%7Buid+background_color_picker+text_color_picker+...SolumCategoryFragment+...CategoryFragment+__typename%7D__typename%7Dproducts%28pageSize%3A%24pageSize+currentPage%3A%24currentPage+filter%3A%24filters+sort%3A%24sort%29%7Bitems%7Bid+uid+name+...galleryItemStorefrontFragment+__typename%7Dpage_info%7Btotal_pages+__typename%7Dtotal_count+...SolumProductsFragment+...ProductsFragment+__typename%7D%7Dfragment+galleryItemStorefrontFragment+on+ProductInterface%7Bid+uid+on_sale_status+__typename%7Dfragment+ProductsFragment+on+Products%7Bitems%7Bid+uid+name+price_range%7Bmaximum_price%7Bfinal_price%7Bcurrency+value+__typename%7Dregular_price%7Bcurrency+value+__typename%7Ddiscount%7Bamount_off+__typename%7D__typename%7D__typename%7Dsku+small_image%7Burl+__typename%7Dstock_status+rating_summary+__typename+url_key%7Dpage_info%7Btotal_pages+__typename%7Dtotal_count+__typename%7Dfragment+SolumCategoryFragment+on+CategoryTree%7Buid+description+cms_content+image+name+product_count+__typename%7Dfragment+CategoryFragment+on+CategoryTree%7Buid+meta_title+meta_keywords+meta_description+__typename%7Dfragment+SolumProductsFragment+on+Products%7Bitems%7Buid+categories%7Buid+name+__typename%7Dprice_range%7Bminimum_price%7Bregular_price%7Bcurrency+value+__typename%7Dfinal_price%7Bcurrency+value+__typename%7Ddiscount%7Bpercent_off+amount_off+__typename%7D__typename%7Dmaximum_price%7Bregular_price%7Bcurrency+value+__typename%7Dfinal_price%7Bcurrency+value+__typename%7D__typename%7D__typename%7Dshort_description%7Bhtml+__typename%7Durl_suffix+...on+ConfigurableProduct%7Buid+configurable_options%7Buid+attribute_code+attribute_id+is_swatch_visible_in_list+label+values%7Buid+default_label+label+store_label+use_default_value+value_index+swatch_data%7B...on+ImageSwatchData%7Bthumbnail+__typename%7Dvalue+__typename%7D__typename%7D__typename%7Dvariants%7Battributes%7Buid+code+value_index+__typename%7Dproduct%7Buid+sku+short_description%7Bhtml+__typename%7Dprice_range%7Bmaximum_price%7Bregular_price%7Bcurrency+value+__typename%7Dfinal_price%7Bcurrency+value+__typename%7D__typename%7Dminimum_price%7Bregular_price%7Bcurrency+value+__typename%7Dfinal_price%7Bcurrency+value+__typename%7Ddiscount%7Bpercent_off+amount_off+__typename%7D__typename%7D__typename%7Dsmall_image%7Blabel+url+__typename%7Dstock_status+__typename%7D__typename%7D__typename%7D__typename%7D__typename%7D&operationName=GetCategories&variables=%7B%22currentPage%22%3A1%2C%22id%22%3A%22NTgx%22%2C%22filters%22%3A%7B%22on_sale_status%22%3A%7B%22eq%22%3A%221%22%7D%2C%22category_uid%22%3A%7B%22eq%22%3A%22NTgx%22%7D%7D%2C%22pageSize%22%3A24%2C%22sort%22%3A%7B%22position%22%3A%22ASC%22%7D%7D