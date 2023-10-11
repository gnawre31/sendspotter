import json
from datetime import datetime
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from dotenv import load_dotenv
import os
load_dotenv()



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


            




    
        





if __name__ =="__main__":
    sheets = SheetsAPI()
    # sheets.testAppend()
    pass
