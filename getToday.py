
from SheetsAPI import SheetsAPI
from datetime import date
import json



if __name__ == "__main__":
    # get all rows
    sheets = SheetsAPI()
    df = sheets.getAllDataByRange("A:R")

    # filter dataframe by rows == today's date

    today = str(date.today())
    today_df = df[df['date'] == today]

    # Group by unique combinations of the specified columns
    grouped = today_df.groupby(['matched_brand', 'matched_product_name', 'gender', 'date'])
    result = {"data": []}



    # # Iterate through the groups and create dict 
    for (matched_brand, matched_product_name, gender, date_val), group in grouped:
        # grouped['id'] = matched_brand + '-' + matched_product_name + '-' + gender
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
            "product_name": matched_product_name,
            "gender": gender,
            "date": date_val,
            "retailers": retailers
        }
        
        result["data"].append(data_entry)

    # Now 'result' contains the desired dictionary structure
    final_dict = {"data": result["data"]}
    




    

        

    