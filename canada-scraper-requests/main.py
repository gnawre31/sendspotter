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
    'scarpa',
    'la sportiva',
    'black diamond',
    'boreal',
    'butora',
    'evolv',
    'five ten',
    'mad rock',
    'ocun',
    'red chili'
    'tenaya',
    'unparallel'
]
SCARPA = [
    'mago',
    'boostic',
    'booster',
    'vapor v',
    'vapor',
    'vapor s',
    'veloce',
    'veloce lace',
    'reflex',
    'velocity',
    'reflex v',
    'drago',
    'drago lv',
    'chimera',
    'furia s',
    'furia air',
    'instinct vs',
    'instinct',
    'instinct sr',
    'instinct vsr',
    'arpia',
    'maestro eco',
    'maestro alpine',
    'maestro mid eco',
    'helix',
    'origin',
    'jungle',
    'force v',
    'generator mid',
    'generator',
    'quantix sf',
    'quantic',
]
LA_SPORTIVA = [
    'miura vs',
    'miura',
    'tc pro',
    'katana lace',
    'mantra',
    'skwama vegan',
    'tarantula boulder',
    'tarantula',
    'tarantulace',
    'aragon',
    'finale',
    'kubo',
    'mythos eco',
    'mythos',
    'cobra 4:99',
    'cobra eco',
    'skwama',
    'otaki',
    'solution comp',
    'solution',
    'theory',
    'futura',
    'genius',
    'testarossa',
    'mega ice evo',
    'python'
]
BLACK_DIAMOND = [
    'momentum',
    'momentum lace',
    'shadow',
    'shadow lv',
    'method',
    'method s',
    'aspect',
    'aspect pro',
    'zone',
    'focus'
]
BOREAL = [
    'synergy',
    'ace',
    'satori',
    'crux lace',
    'crux',
    'ninja',
    'diabolo',
    'diabola'
    'mutant',
    'beta eco',
    'beta',
    'dharma',
    'joker',
    'joker lace',
    'joker plus',
    'alpha',
    'silex'
]
BUTORA = [
    'gomi spinter',
    'acro comp',
    'altura',
    'mantra',
    'endeavor',
    'habara',
    'new bora',
    'brava'
]
EVOLV = [
    'defy lace',
    'defy',
    'eldo z',
    'elektra lace',
    'elektra',
    'geshido lace',
    'geshido',
    'kira',
    'kronos',
    'phantom',
    'phantom lv',
    'rave',
    'shaktra',
    'shaman',
    'shaman lace',
    'shaman lace lv',
    'shaman lv',
    'shaman pro',
    'shaman pro lv',
    'the general',
    'titan',
    'venga',
    'yosemite bum',
    'yosemite bum lv',
    'zenist',
    'zenist pro',
    'zenist pro lv'
]
FIVE_TEN = [
    'kirigami',
    'crawe',
    'niad lace',
    'niad moccasym',
    'niad vcs',
    'hiangle pro',
    'hiangle',
    'rogue vcs',
    'aleon',
    'quantum vcs',
    'asym',
    'anasazi',
    'grandstone',
]
MAD_ROCK = [
    'drone comp lv',
    'drone comp hv',
    'redline strap',
    'shark 2.0',
    'drone lv black',
    'drone hv black',
    'drone lv',
    'drone cs hv',
    'drone cs lv',
    'drone hv',
    'rover',
    'haywire',
    'lotus',
    'redline lace',
    'weaver',
    'remora',
    'remora lv',
    'remora hv',
    'remora tokyo',
    'm5',
    'lyra',
    'demon 2.0',
    'agama',
    'flash 2.0',
    'drifter',
    'pulse negative',
    'pulse positive',
    'badger',
   'phoenix'
]
OCUN = [
    'fury',
    'diamond',
    'ozone',
    'ozone hv',
    'bullit',
    'havoc',
    'jett qc',
    'jett lu',
    'jett crack',
    'pearl 20th anniversary',
    'advancer qc',
    'advancer lu',
    'striker lu',
    'striker qc',
    'rival',
    'rental',
    'ribbit'
]
RED_CHILI = [
    'sensor',
    'mystix',
    'voltage 2',
    'voltage lv',
    'voltage lace',
    'fusion',
    'fusion lv',
    'puzzle',
    'circuit lv',
    'circuit',
    'ventic air lace',
    'sausalito',
    'session 4 s',
    'session',
    'pulpo',
    'session air'
]
TENAYA = [
    'indalo',
    'mastia',
    'mundaka',
    'lati',
    'tarifa',
    'oasi',
    'oasi lv',
    'ra',
    'masai',
    'inti',
    'tatanka',
    'aqua+',
    'arai',
    'tanta',
    'tanta laces',
    'tanta lx'
]
UNPARALLEL = [
    'up pivot',
    'souped up',
    'engage lace up',
    'tn pro lv',
    'tn pro',
    'flagship lv',
    'flagship',
    'up-rise pro',
    'leopard 2',
    'up duel',
    'lyra',
    'regulus',
    'regulus lv',
    'vim',
    'sirius lace',
    'sirius lace lv',
    'newtro vcs',
    'up rise vcs',
    'up rise vcs lv',
    'up rise zero vcs lv',
    'up lace',
    'up lace lv',
    'engage vcs',
    'engage vcs lv',
    'newtro lace',
    'vega',
    'mocc',
    'grade mocc',
    'grade engage',
    'hold up slipper',
    'hold up vcs'
]
brandConstDict = {
    'scarpa': SCARPA,
    'la sportiva': LA_SPORTIVA,
    'black diamond':BLACK_DIAMOND,
    'boreal':BOREAL,
    'butora':BUTORA,
    'evolv':EVOLV,
    'five ten':FIVE_TEN,
    'mad rock':MAD_ROCK,
    'ocun':OCUN,
    'red chili':RED_CHILI,
    'tenaya':TENAYA,
    'unparallel':UNPARALLEL,
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
                product.discount_pct
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
            # check if men, women, or unisex are included in name
            femaleNouns = ['women', 'womens', 'women\'s', 'female', 'wmn']
            maleNouns = ['men', 'mens', 'men\'s', 'male']

            if any(word in self.formatted_product_name for word in femaleNouns):
                self.gender = 'f'
                self.formatted_product_name = self.formatted_product_name.replace("women\'s","")
                self.formatted_product_name = self.formatted_product_name.replace("womens","")
                self.formatted_product_name = self.formatted_product_name.replace("women","")
                self.formatted_product_name = self.formatted_product_name.replace("wmn","")

            elif any(word in self.formatted_product_name for word in maleNouns):
                self.gender = 'm'
                self.formatted_product_name = self.formatted_product_name.replace("men\'s","")
                self.formatted_product_name = self.formatted_product_name.replace("mens","")
                self.formatted_product_name = self.formatted_product_name.replace("men","")
            
            else:
                self.gender = 'u'
                self.formatted_product_name = self.formatted_product_name.replace("unisex","")

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

        retailer.addProducts(products)
        currPage += 1

    return retailer
    



