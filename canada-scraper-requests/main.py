from tempfile import mkdtemp
import requests
from bs4 import BeautifulSoup
from datetime import date
import hashlib
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
    'Red Chili'
    'tenaya',
    'Unparallel'
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
    'Python'
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
    'Diabola'
    'Mutant',
    'Beta Eco',
    'Beta',
    'Dharma',
    'Joker',
    'Joker Lace',
    'Joker Plus',
    'Alpha',
    'Silex'
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
    'Redline Strap'
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
        climbOn = scrapeClimbOn()
        climbOn.saveToSheets()

        madRock = scrapeMadRock()
        madRock.saveToSheets()

        return "success"
    except:
        return "fail"

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
            for color in colors:
                self.formatted_product_name = self.formatted_product_name.replace(color,"")
            
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
            fuzz_ratio = fuzz.ratio(str.lower(), s)
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
    
def scrapeClimbOn():

    """
    Crawls through all pages, extracting details for products on sale 

    :return: res: product details for all products on sale 
    :returnType: List
    """

    retailer = Retailer(retailer="Climb On Squamish", country="Canada", currency="CAD")

    LINK = "https://climbonequipment.com/collections/climbing-shoes"
    SITE = "https://climbonequipment.com"

    response = requests.get(LINK) 
    soup = BeautifulSoup(response.text, "html.parser")
    pageDiv = soup.find("div", {"class": "pagination"})
    pageNums = pageDiv.find_all("span", {"class":"page"})

    currPage = 1
    lastPage = int(pageNums[-1].text)


    while currPage <= lastPage:
        
        url = f'{LINK}?page={currPage}'
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, "html.parser")

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

            imgDiv = listing.find("div", {"class":"grid__item-image-wrapper"})
            product.img_url = "https:" + imgDiv.find("img")['src']

        retailer.addProducts(products)
        currPage += 1

    return retailer

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
     

    response = requests.get(LINK) 
    # print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    pageDiv = soup.find("div", {"class": "pagination"})
    pageNums = pageDiv.find_all("span", {"class":"page"})
    lastPage = len(pageNums)


    while currPage <= lastPage:
        
        url = f'{LINK}?page={currPage}'
        response = requests.get(url) 
        soup = BeautifulSoup(response.text, "html.parser")
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
        retailer.addProducts(products)
        currPage += 1

    return retailer

# if __name__ == "__main__":
#     climbon = scrapeClimbOn()
#     climbon.printList()
#     madrock = scrapeMadRock()
#     madrock.printList()