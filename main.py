import pandas as pd 
from database import DatabaseManager
from analytics import ECommerceAnalytics


filepath="data/online_retail.csv"

df=pd.read_csv(filepath)

print("__First 5 rows__")
print(df.head())

print("__Column Information__")
print(df.info())

# Clean the data...
df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])

df=df.dropna(subset=['CustomerID'])

df['Description'] =df['Description'].fillna('UNKNOWN PRODUCT')

print("\n__After Cleaning__")
print(f"Total Rows: {len(df)}")
print(df.info())

if __name__=="__main__":
    try:

        print("\n[INFO] Initializing DatabaseManager...")
        db=DatabaseManager()

        print("[INFO] Querying top selling products...")
        db.save_cleaned_data_to_db(df)

        print("\n[INFO] Initializing Analytics Engine...")
        analytics = ECommerceAnalytics()

        print("[INFO] Querying top selling products...")
        top_products =analytics.get_top_selling_products(limit=5)

        print("\n==============================")
        print("\n__top 5 selling products__")
        print("\n==============================")
        print(top_products)



        print("[INFO] Querying top spending customers...")
        top_spenders =analytics.get_top_spenders(limit=5)


        print("\n==============================")
        print("\n__top 5 spenders__")
        print("\n==============================")
        print(top_spenders)

    except Exception as e :
        print(f"\n[ERROR OCCURRED]: {e}")
