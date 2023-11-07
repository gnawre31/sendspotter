from tempfile import mkdtemp

import pandas as pd
import json
from datetime import date
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

import os
import json
import urllib.parse
import boto3


s3 = boto3.client('s3')

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

def handler(event=None, context=None):

    try:
        # get all rows
        sheets = SheetsAPI()
        # print(sheets.SHEET_ID)
        df = sheets.getAllDataByRange(sheets.ALL_RANGE)


        print("all df", df.shape)

        # filter dataframe by rows == today's date

        today = str(date.today())
        print(today)
        today_df = df[df['date'] == today]

        print("all df", today_df.shape)


        # # Group by unique combinations of the specified columns
        grouped = today_df.groupby(['matched_brand', 'id', 'matched_product_name', 'gender', 'date'])
        result = {"data": []}

        # # # Iterate through the groups and create dict 
        for (matched_brand, id, matched_product_name, gender, date_val), group in grouped:
            retailers = []
            
            for _, row in group.iterrows():
                retailer_info = {
                    "retailer": row['retailer'],
                    "retailer_id": row['retailer_id'],
                    "og_price": float(row['og_price']),
                    "sale_price": float(row['sale_price']),
                    "discount_pct": int(row['discount_pct']),
                    "web_url": row['web_url'],
                    "img_url": row['img_url']
                }
                retailers.append(retailer_info)
            
            data_entry = {
                "brand": matched_brand,
                "id": id,
                "product_name": matched_product_name,
                "gender": gender,
                "date": date_val,
                "retailers": retailers
            }
            
            result["data"].append(data_entry)

        # # Now 'result' contains the desired dictionary structure
        final_dict = {"data": result["data"], "datetime": str(datetime.now())}
        


        # print(res)
        bucket = 'sendspotter'

        filename = 'discounted_shoes_today_CAN.json'
    
        uploadByteStream = bytes(json.dumps(final_dict).encode('UTF-8'))
        
        s3.put_object(Bucket=bucket, Key=filename, Body=uploadByteStream)

        return "success"
    except:
        return "fail"

