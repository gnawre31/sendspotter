from datetime import date
import hashlib
from rapidfuzz import fuzz

from consts import BRANDS
from consts import brandConstDict

from SheetsAPI import SheetsAPI


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
        self.img_url = None

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
            self.discount_pct is None or 
            self.img_url is None
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

            # remove color
            colors = ['blue', 'yellow','orange','purple','charcoal','black','white','green','red','brown','pink','silver']
            for color in colors:
                self.formatted_product_name = self.formatted_product_name.replace(color,"")

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
                self.formatted_product_name = self.formatted_product_name.replace(" men\'s","")
                self.formatted_product_name = self.formatted_product_name.replace(" mens","")
                self.formatted_product_name = self.formatted_product_name.replace(" men","")
            
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

            

    


if __name__ == "__main__":
    # test code
    # retailer = Retailer(retailer="Test Retailer", country="Canada", currency="CAD") 
    # print(retailer.retailer_id)
    pass


