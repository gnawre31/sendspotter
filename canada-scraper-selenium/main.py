from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import date
import hashlib
import time
from rapidfuzz import fuzz

import pandas as pd
import json
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

import os


BRANDS = [
    'Scarpa',
    'La Sportiva',
    'Black Diamond',
    'Boreal',
    'Butora',
    'Evolv',
    'Five Ten',
    'Mad Rock',
    'Ocun',
    'Red Chili',
    'Tenaya',
    'Unparallel',
    'SoiLL'
]


SCARPA = [
    'Mago',
    'Boostic',
    'Booster',
    'Vapor V',
    'Vapor',
    'Vapor S',
    'Veloce',
    'Veloce Lace',
    'Reflex',
    'Velocity',
    'Reflex V',
    'Drago',
    'Drago LV',
    'Chimera',
    'Furia S',
    'Furia Air',
    'Instinct VS',
    'Instinct',
    'Instinct SR',
    'Instinct VSR',
    'Arpia',
    'Maestro Eco',
    'Maestro Alpine',
    'Maestro Mid Eco',
    'Helix',
    'Origin',
    'Jungle',
    'Force V',
    'Generator Mid',
    'Generator',
    'Quantix SF',
    'Quantic',
]
LA_SPORTIVA = [
    'Miura VS',
    'Miura',
    'TC Pro',
    'Katana Lace',
    'Mantra',
    'Skwama Vegan',
    'Tarantula Boulder',
    'Tarantula',
    'Tarantulace',
    'Aragon',
    'Finale',
    'Kubo',
    'Mythos Eco',
    'Mythos',
    'Cobra 4:99',
    'Cobra Eco',
    'Skwama',
    'Otaki',
    'Solution Comp',
    'Solution',
    'Theory',
    'Futura',
    'Genius',
    'Testarossa',
    'Mega Ice Evo',
    'Python',
    'Stickit'
]

BLACK_DIAMOND = [
    'Momentum',
    'Momentum Lace',
    'Shadow',
    'Shadow LV',
    'Method',
    'Method S',
    'Aspect',
    'Aspect Pro',
    'Zone',
    'Zone LV',
    'Focus',
    'Session'
]

BOREAL = [
    'Synergy',
    'Ace',
    'Satori',
    'Crux Lace',
    'Crux',
    'Ninja',
    'Diabolo',
    'Diabola',
    'Mutant',
    'Beta Eco',
    'Beta',
    'Dharma',
    'Joker',
    'Joker Lace',
    'Joker Plus',
    'Alpha',
    'Silex',
    'Ballet'
]

BUTORA = [
    'Gomi Spider',
    'Acro Comp',
    'Altura',
    'Mantra',
    'Endeavor',
    'Habara',
    'New Bora',
    'Brava'
]

EVOLV = [
    'Defy Lace',
    'Defy',
    'Eldo Z',
    'Elektra Lace',
    'Elektra',
    'Geshido Lace',
    'Geshido',
    'Kira',
    'Kronos',
    'Phantom',
    'Phantom LV',
    'Rave',
    'Shaktra',
    'Shaman',
    'Shaman Lace',
    'Shaman Lace LV',
    'Shaman LV',
    'Shaman Pro',
    'Shaman Pro LV',
    'The General',
    'Titan',
    'Venga',
    'Yosemite Bum',
    'Yosemite Bum LV',
    'Zenist',
    'Zenist Pro',
    'Zenist Pro LV'
]

FIVE_TEN = [
    'Kirigami',
    'Crawe',
    'Niad Lace',
    'Niad Moccasym',
    'Niad VCS',
    'Hiangle Pro',
    'Hiangle',
    'Rogue VCS',
    'Aleon',
    'Quantum VCS',
    'Asym',
    'Anasazi',
    'Anasazi VCS',
    'Grandstone',
]

MAD_ROCK = [
    'Drone Comp LV',
    'Drone Comp HV',
    'Redline Strap',
    'Shark 2.0',
    'Drone LV Black',
    'Drone HV Black',
    'Drone LV',
    'Drone CS HV',
    'Drone CS LV',
    'Drone HV',
    'Rover',
    'Haywire',
    'Lotus',
    'Redline Lace',
    'Redline Strap',
    'Weaver',
    'Remora',
    'Remora LV',
    'Remora HV',
    'Remora Tokyo',
    'M5',
    'Lyra',
    'Demon 2.0',
    'Agama',
    'Flash 2.0',
    'Drifter',
    'Pulse Negative',
    'Pulse Positive',
    'Badger',
    'Phoenix'
]

OCUN = [
    'Fury',
    'Diamond',
    'Ozone',
    'Ozone HV',
    'Bullit',
    'Havoc',
    'Jett QC',
    'Jett LU',
    'Jett Crack',
    'Pearl 20th Anniversary',
    'Advancer QC',
    'Advancer LU',
    'Striker LU',
    'Striker QC',
    'Rival',
    'Rental',
    'Ribbit'
]

RED_CHILI = [
    'Sensor',
    'Mystix',
    'Voltage 2',
    'Voltage LV',
    'Voltage Lace',
    'Fusion',
    'Fusion LV',
    'Puzzle',
    'Circuit LV',
    'Circuit',
    'Ventic Air Lace',
    'Sausalito',
    'Session 4 S',
    'Session',
    'Pulpo',
    'Session Air'
]

TENAYA = [
    'Indalo',
    'Mastia',
    'Mundaka',
    'Lati',
    'Tarifa',
    'Oasi',
    'Oasi LV',
    'Ra',
    'Masai',
    'Inti',
    'Tatanka',
    'Aqua+',
    'Arai',
    'Tanta',
    'Tanta Laces',
    'Tanta LX'
]

UNPARALLEL = [
    'UP Pivot',
    'Souped UP',
    'Engage Lace UP',
    'TN Pro LV',
    'TN Pro',
    'Flagship LV',
    'Flagship',
    'UP Rise Pro',
    'Leopard 2',
    'UP Duel',
    'Lyra',
    'Regulus',
    'Regulus LV',
    'Vim',
    'Sirius Lace',
    'Sirius Lace LV',
    'Newtro VCS',
    'UP Rise VCS',
    'UP Rise VCS LV',
    'UP Rise Zero VCS LV',
    'UP Lace',
    'UP Lace LV',
    'Engage VCS',
    'Engage VCS LV',
    'Newtro Lace',
    'Vega',
    'UP Mocc',
    'Grade Mocc',
    'Grade Engage',
    'Hold Up Slipper',
    'Hold Up VCS'
]

SOILL = [
    'The Onset',
    'New Zero',
    'Free Range LV',
    'Street LV',
    'The Street',
    'Momoa Pro',
    'Momoa Pro LV',
    'Free Range Pro',
    'Street',
    'Stay',
    'Catch',
    'The Runner LV',
    'The Runner'
]

brandConstDict = {
    'Scarpa': SCARPA,
    'La Sportiva': LA_SPORTIVA,
    'Black Diamond':BLACK_DIAMOND,
    'Boreal':BOREAL,
    'Butora':BUTORA,
    'Evolv':EVOLV,
    'Five Ten':FIVE_TEN,
    'Mad Rock':MAD_ROCK,
    'Ocun':OCUN,
    'Red Chili':RED_CHILI,
    'Tenaya':TENAYA,
    'Unparallel':UNPARALLEL,
    'SoiLL': SOILL
}


class SheetsAPI():
    def __init__(self):
        """
        Connects to google apis and initiates google sheets service
        """

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        service_account_info = {
            "type": os.getenv("TYPE"),
            "project_id": os.getenv("PROJECT_ID"),
            "private_key_id": os.getenv("PRIVATE_KEY_ID"),
            "private_key": os.getenv("PRIVATE_KEY").replace(r'\n','\n'),
            "client_email": os.getenv("CLIENT_EMAIL"),
            "client_id": os.getenv("CLIENT_ID"),
            "auth_uri": os.getenv("AUTH_URI"),
            "token_uri": os.getenv("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
            "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
        }
        service_account_info = json.dumps(service_account_info)
        service_account_info = json.loads(service_account_info)
        credentials=Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        self.SHEET_ID = os.getenv("SHEET_ID")
        self.ALL_RANGE = os.getenv("ALL_RANGE")
        self.ID_RANGE = os.getenv("ID_RANGE")
        self.sheets = service.spreadsheets()

    def getAllDataByRange(self, range):
        data = None
        try:
            result = self.sheets.values().get(spreadsheetId=self.SHEET_ID, range=range).execute()
            values = result.get('values', [])
            if values:
                data = pd.DataFrame(values[1:], columns=values[0])

        except TypeError as err:
            print(err)
        
        return data

    def testAppend(self):
        values = [[23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]]
        body = {'values': values}
        value_input_option = 'RAW'
        self.sheets.values().append(body=body, spreadsheetId=self.SHEET_ID, range=self.ALL_RANGE,valueInputOption=value_input_option).execute()
    

    #1 website data --> google sheets
    #2 grab data from google sheets --> API endpoints
    #3 call api endpoints --> front end
        
    
    def insertScrapedRetailer(self, retailer):
        

        ids = self.getAllDataByRange(self.ID_RANGE).stack().values

        values = []

        for product in retailer.products:

            # check if entry already recorded 
            if product.id in ids:
                continue
            
            data = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                retailer.retailer_id,
                retailer.retailer,
                retailer.date,
                retailer.country,	
                retailer.currency,	
                product.id,
                product.web_url,	
                product.matched_brand,	
                product.scraped_brand,	
                product.matched_product_name,	
                product.formatted_product_name,	
                product.scraped_product_name,	
                product.gender,	
                product.og_price,	
                product.sale_price,	
                product.discount_pct,
                product.img_url
            ]
            values.append(data)
        body = {'values':values}

        # print(body)

        value_input_option = 'RAW'
        self.sheets.values().append(body=body, spreadsheetId=self.SHEET_ID, range=self.ALL_RANGE,valueInputOption=value_input_option).execute()

def handler(event=None, context=None):
    try:
        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService("/opt/chromedriver")

        options.binary_location = '/opt/chrome/chrome'
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")

        chrome = webdriver.Chrome(options=options, service=service)

        try:
            sail = scrapeSail(chrome)
            sail.saveToSheets()
        except:
            print("500 - failed to scrape Sail")
            raise

        try:
            lastHunt, altitude = scrapeLastHuntAltitude(chrome)
            lastHunt.saveToSheets()
            altitude.saveToSheets()
        except:
            print("500 - failed to scrape The Last Hunt, Altitude")
            raise

        try:
            vpo = scrapeVPO(chrome)
            vpo.saveToSheets()
        except:
            print("500 - failed to scrape VPO")
            raise

        try:
            mec = scrapeMEC(chrome)
            mec.saveToSheets()

        except Exception as e:
            print("500 - failed to scrape MEC")   
            print(e)
            raise

        try:
            blocShop = scrapeBlocShop(chrome)
            blocShop.saveToSheets()
        except:
            print("500 - failed to scrape MEC")   
            raise
        try:
            monodSports = scrapeMonodSports(chrome)
            monodSports.saveToSheets()
        except:
            print("500 - failed to scrape monod sports")   
            raise

        return "200 - sail, vpo, mec, blocshop, last hunt, altitude"
    except:
        return "500 failed" 

    


class Retailer():
    def __init__(self, retailer, country, currency):
        self.retailer_id = hashlib.sha1(str.encode(retailer)).hexdigest()
        self.products = []
        self.date = date.today().strftime('%Y-%m-%d')
        self.retailer = retailer
        self.country = country
        self.currency = currency
    
    def addProducts(self, products):
        for product in products:
            if product.validate() == True:
                self.products.append(product)

    def validate(self):
        if (
            self.retailer_id is None or
            self.retailer is None or 
            self.country is None or
            self.currency is None or
            self.date is None or 
            len(self.products) == 0
        ):
            return False
        return True
    
    def printList(self):
        
        for product in self.products:
            product.printProduct()

    def saveToSheets(self):
        if self.validate() == True:
            sheets = SheetsAPI()
            sheets.insertScrapedRetailer(self)
            
class Product():
    def __init__(self):
        self.id = None
        self.web_url = None
        self.matched_brand = None
        self.scraped_brand = None
        self.matched_product_name = None
        self.formatted_product_name = None
        self.scraped_product_name = None
        self.gender = None
        self.og_price = None
        self.sale_price = None
        self.discount_pct = None

    def validate(self):
        if (
            self.id is None or 
            self.web_url is None or 
            self.matched_brand is None or 
            self.scraped_brand is None or 
            self.matched_product_name is None or 
            self.formatted_product_name is None or 
            self.scraped_product_name is None or 
            self.gender is None or 
            self.og_price is None or 
            self.sale_price is None or 
            self.discount_pct is None
        ):
            return False
        else:
            return True
    
    def getGender(self):
        """
        Extracts gender details from scraped product name and set the gender attribute
        """
        if self.scraped_product_name is not None:

            # set to lower case and replace generic words
            self.formatted_product_name = self.scraped_product_name.lower()
            self.formatted_product_name = self.formatted_product_name.replace("climbing","").replace("shoes","").replace("shoe","").replace("rock","").replace("-","")
            
            colors = ['blue', 'yellow','orange','purple','charcoal','black','white','green','red','brown','pink','silver']
            for c in colors:
                self.formatted_product_name = self.formatted_product_name.replace(c,"")

            # check if men, women, or unisex are included in name
            femaleNouns = ['women', 'womens', 'women\'s', 'female', 'wmn', 'w\'s']
            maleNouns = ['men', 'mens', 'men\'s', 'male','m\'s']

            if any(word in self.formatted_product_name for word in femaleNouns):
                self.gender = 'f'
                self.formatted_product_name = self.formatted_product_name.replace("women\'s","")
                self.formatted_product_name = self.formatted_product_name.replace("womens","")
                self.formatted_product_name = self.formatted_product_name.replace("women","")
                self.formatted_product_name = self.formatted_product_name.replace("wmn","")
                self.formatted_product_name = self.formatted_product_name.replace("w\'s","")


            elif any(word in self.formatted_product_name for word in maleNouns):
                self.gender = 'm'
                self.formatted_product_name = self.formatted_product_name.replace("men\'s","")
                self.formatted_product_name = self.formatted_product_name.replace("mens","")
                self.formatted_product_name = self.formatted_product_name.replace("men","")
                self.formatted_product_name = self.formatted_product_name.replace("m\'s","")

            
            else:
                self.gender = 'u'
                self.formatted_product_name = self.formatted_product_name.replace("unisex","")
                self.formatted_product_name = self.formatted_product_name.replace("children's","")
                self.formatted_product_name = self.formatted_product_name.replace("children","")
                self.formatted_product_name = self.formatted_product_name.replace("kid's","")
                self.formatted_product_name = self.formatted_product_name.replace("kids","")
                self.formatted_product_name = self.formatted_product_name.replace("kid","")

            self.formatted_product_name = self.formatted_product_name.strip()   
        
    def getMatchedBrand(self):
        """
        Data cleaning: fuzzy matches against a standardized list of shoe brands.
        """
        if self.scraped_brand is not None:
            matched_brand = self.getBestMatch(self.scraped_brand, BRANDS)
            self.matched_brand = matched_brand
    
    def getMatchedProduct(self):
        """
        Data cleaning:
        Note: requires getGender() and matchBrand() to be run first
        """
        if self.formatted_product_name is not None and self.matched_brand is not None:
            product_list = brandConstDict[self.matched_brand]
            matched_product = self.getBestMatch(self.formatted_product_name, product_list)
            self.matched_product_name = matched_product

    def getBestMatch(self, str, listOfStrs):
        best_match_ratio = -1
        best_match_str = None
        for s in listOfStrs:
            fuzz_ratio = fuzz.ratio(str.lower(), s.lower())
            if fuzz_ratio > best_match_ratio:
                best_match_ratio = fuzz_ratio
                best_match_str = s
        
        return best_match_str
    
    def generateID(self, retailer):
        if (
            self.matched_brand is not None and
            self.matched_product_name is not None and
            self.gender is not None and
            self.discount_pct is not None and
            retailer.retailer is not None and
            retailer.date is not None and 
            retailer.country is not None
        ):
            s = retailer.retailer + str(retailer.date) + retailer.country + self.matched_brand + self.matched_product_name + self.gender + str(self.discount_pct)
            self.id = hashlib.sha1(str.encode(s)).hexdigest()
    
    def printProduct(self):
            print("PRODUCT ------------------------------------")
            print("id: \t".expandtabs(30), self.id)
            print("web_url: \t".expandtabs(30), self.web_url)
            print("scraped_brand: \t".expandtabs(30), self.scraped_brand)
            print("matched_brand: \t".expandtabs(30), self.matched_brand)
            print("scraped_product_name: \t".expandtabs(30), self.scraped_product_name)
            print("formatted_product_name: \t".expandtabs(30), self.formatted_product_name)
            print("matched_product_name: \t".expandtabs(30), self.matched_product_name)
            print("gender: \t".expandtabs(30), self.gender)
            print("sale_price: \t".expandtabs(30), self.sale_price)
            print("og_price: \t".expandtabs(30), self.og_price)
            print("discount_pct: \t".expandtabs(30), self.discount_pct)
            print("img_url: \t".expandtabs(30), self.img_url)
            print("--------------------------------------------")

def getBrandLenFromStr(product_title):
    product_title = product_title.lower()
    matched = ""
    for b in BRANDS:
        if b.lower() in product_title:
            matched = b
            break

    return len(matched)

def scrapeSail(chrome):

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Sail", country="Canada", currency="CAD")


    LINK = "https://www.sail.ca/en/outdoor-gear/climbing/climbing-shoes#/filter:ss_special_price:Yes"
    chrome.get(LINK)
    time.sleep(15)


    soup = BeautifulSoup(chrome.page_source, "html.parser")

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

        imgDiv = listing.find("span",{"class":"product-image-wrapper"})
        product.img_url = imgDiv.find("img")['src']


        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)

    retailer.addProducts(products)
    return retailer

def scrapeLastHuntAltitude(chrome):

    lastHunt = Retailer(retailer="The Last Hunt", country="Canada", currency="CAD")
    altitude = Retailer(retailer="Altitude Sports", country="Canada", currency="CAD")
    retailers = [lastHunt, altitude]

    links = [
        ["https://www.thelasthunt.com/collections/gear-climbing-climbing-shoes","https://www.thelasthunt.com" ],
        ["https://www.altitude-sports.com/collections/gear-climbing-climbing-shoes#?filter.on_sale=Yes","https://www.altitude-sports.com"]
    ]

    for idx, l in enumerate(links):
        retailer = retailers[idx]
        LINK = l[0]
        SITE = l[1]
        chrome.get(LINK)
        time.sleep(5)
        soup = BeautifulSoup(chrome.page_source, "html.parser")
        products = []
        listings = soup.find_all("li", {"class": "ss-product"})
        # all products are discounted on this page

        for listing in listings:

            product = Product()

            product.web_url = SITE + listing.find("a", {"class": "ss-product__info__manufacturer"})['href']
            product.scraped_brand = listing.find("a", {"class": "ss-product__info__manufacturer"}).text.strip()
            product.scraped_product_name = listing.find("h3", {"class": "ss-product__info__name"}).text.strip()
            product.sale_price = float(listing.find("span",{"class":"ss-product__price--special"}).text.replace("$","").replace("CAN ","").strip())
            product.og_price = float(listing.find("span",{"class":"ss-product__price--old"}).text.replace("$","").replace("CAN ","").strip())
            product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)
            product.img_url = listing.find("img",{"class":"ss-product__img"})['src']

            # skip approach shoes
            if "approach" in product.scraped_product_name.lower() or "leather" in product.scraped_product_name.lower() or "tx2" in product.scraped_product_name.lower() or "hiking" in product.scraped_product_name.lower():
                continue

            product.getGender()
            product.getMatchedBrand()
            product.getMatchedProduct()
            product.generateID(retailer)

            products.append(product)
        retailer.addProducts(products)

    return retailers

def scrapeVPO(chrome):

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="VPO", country="Canada", currency="CAD")
    LINK = "https://vpo.ca/category/181/shoes"
    SITE = "https://vpo.ca"

    currPage = 1
    lastPage = 1

    

    while currPage <= lastPage:
        url = f'{LINK}?pagenum={currPage}'
        chrome.get(url)
        time.sleep(5)
        soup = BeautifulSoup(chrome.page_source, "html.parser")

        if currPage == 1:
            pages = soup.find_all("li",{"class":"ss-page"})
            lastPage = len(pages)-1
        
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
        retailer.addProducts(products)
        currPage+= 1

    return retailer

def scrapeMEC(chrome):
    retailer = Retailer(retailer="MEC", country="Canada", currency="CAD")

    LINK = "https://www.mec.ca/en/products/climbing/climbing-footwear/rock-climbing-shoes/c/1190"
    SITE = "https://www.mec.ca"


    currPage = 1
    lastPage = 1
    while currPage <= lastPage:


        

        url = f'{LINK}?offset={(currPage-1)*32}'

        chrome.get(url)
        time.sleep(10)
        soup = BeautifulSoup(chrome.page_source, "html.parser")
        products = []

        if currPage == 1:
            pageDiv = soup.find("div",{"class":"findify-components--pagination"})
            pages = soup.find_all("a",{"class":"findify-components--pagination__page"})
            lastPage = len(pages)

        listings = soup.find_all("div", {"class": "findify-components--cards--product"})

        for listing in listings:

            isOnClearance = listing.find("div",{"class":"findify-product-sticker-clearance"})
            isOnSale = listing.find("div",{"class":"findify-product-sticker-sale"})

            if isOnClearance is None and isOnSale is None:
                continue

            product = Product()

            product.web_url = SITE + listing.find("a", {"class": "findify-components--cards--product__rating"})["href"]
            product_title = listing.find("h3",{"class":"findify-components--cards--product__title"}).text

            brandLen = getBrandLenFromStr(product_title)
            product.scraped_product_name = product_title[brandLen:].strip()
            product.scraped_brand = product_title[0:brandLen]


            product.og_price = float(listing.find("span",{"class":"findify-components--cards--product--price__compare"}).text.replace("$","").replace(" CAD", ""))
            product.sale_price = float(listing.find("span",{"class":"findify-components--cards--product--price__sale-price"}).text.replace("$","").replace("\n","").replace("from ",""))
            product.discount_pct = round((product.og_price - product.sale_price) / product.og_price * 100)

            imgDiv = listing.find("div", {"class":"findify-components-common--image"})
            product.img_url = imgDiv.find("img")['src']



            product.getGender()
            product.getMatchedBrand()
            product.getMatchedProduct()
            product.generateID(retailer)

            products.append(product)
        retailer.addProducts(products)
        retailer.printList()
        currPage += 1
    return retailer
     
def scrapeBlocShop(chrome):

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

    SITE = "https://shop.blocshop.com"

    for brand in links.keys():
        LINK = links[brand]
        chrome.get(LINK)
        time.sleep(2)

        # scroll down once
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        soup = BeautifulSoup(chrome.page_source, "html.parser")
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

            product.img_url = "https:" + productDIV.find("img", {"class":"image__img"})['src']

            product.getGender()
            product.getMatchedBrand()
            product.getMatchedProduct()
            product.generateID(retailer)

            products.append(product)

        retailer.addProducts(products)
    return retailer

def scrapeMonodSports(chrome):

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Monod Sports", country="Canada", currency="CAD")

    LINK = "https://www.monodsports.com/collections/rock-shoes?sort_by=best-selling&filter.p.m.custom.on_sale=Yes"
    SITE = "https://www.monodsports.com"
    chrome.get(LINK)
    time.sleep(5)
    soup = BeautifulSoup(chrome.page_source, "html.parser")
    products = []
    listings = soup.find_all("div", {"class": "product-grid-item"})

    # all products are discounted on this page

    for listing in listings:

        product = Product()

        product.web_url =  SITE + listing.find("a", {"class": "product__media__holder"})['href']

        product_title = listing.find("a",{"class":"product-grid-item__title"}).text
        brandLen = getBrandLenFromStr(product_title)
        product.scraped_product_name = product_title[brandLen:].strip().replace("(Past Season)","")
        product.scraped_brand = product_title[0:brandLen]

        priceDIV = listing.find("a",{"class":"product-grid-item__price"})
        
        product.sale_price = float(priceDIV.find("span",{"class":"product-grid-item__price__new"}).text.replace("$",""))
        product.og_price = float(priceDIV.find("s").text.replace("$",""))
        product.discount_pct = round((product.og_price - product.sale_price ) / product.og_price * 100)

        product.img_url = "https:" + listing.find("picture").find("source")['data-srcset'].split(', ')[-1].split(" ")[0]

        product.getGender()
        product.getMatchedBrand()
        product.getMatchedProduct()
        product.generateID(retailer)

        products.append(product)
    retailer.addProducts(products)
    return retailer



