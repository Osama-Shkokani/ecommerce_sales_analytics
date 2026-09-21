import pandas as pd 

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


import sqlite3

class DatabaseManager:
    """A class to handle SQLite database operations for E-Commerce analytics."""

    def __init__(self,db_name="data/ecommerce.db"):
        self.db_name=db_name
        self.conn=None
        self.cursor=None

    def connect(self):
        self.conn=sqlite3.connect(self.db_name)
        self.cursor=self.conn.cursor()
        print("Database connected successfully.")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def save_cleaned_data_to_db(self,df):
        """Process DataFrame and save data into normalized SQLite tables."""
        self.connect()

        customer_df=df[['CustomerID']].drop_duplicates().copy()
        customer_df.to_sql('customers', self.conn, if_exists='replace', index=False)
        print("customers table created and populated.")

        products_df=df[['StockCode','Description']].drop_duplicates(subset=['StockCode']).copy()
        products_df.to_sql('products', self.conn,if_exists='replace',index=False)
        print("products table created and populated.")

        transactions_df=df[['InvoiceNo','InvoiceDate','CustomerID','StockCode','Quantity','UnitPrice']].copy()
        transactions_df.to_sql('transactions',self.conn,if_exists='replace',index=False)
        print("transactions table created and populated.")

        self.close()
        
    def get_top_selling_products(self,limit=5):
        """Query the database to find the top-selling products by total quantity sold."""
        self.connect()

        query =f""" 
                SELECT p.StockCode, p.Description, SUM(t.Quantity) as TotalQuantity
                FROM transactions t
                JOIN products p ON t.StockCode=p.StockCode
                GROUP BY p.StockCode, p.Description
                ORDER BY TotalQuantity DESC
                LIMIT {limit};
        """
        result_df=pd.read_sql_query(query,self.conn)
        self.close()
        return result_df

if __name__=="__main__":
    try:

        print("\n[INFO] Initializing DatabaseManager...")
        db=DatabaseManager()

        print("[INFO] Querying top selling products...")
        db.save_cleaned_data_to_db(df)

        print("[INFO] Querying top selling products...")
        top_products =db.get_top_selling_products(limit=5)

        print("\n==============================")
        print("\n__top 5 selling products__")
        print("\n==============================")
        print(top_products)
    except Exception as e :
        print(f"\n[ERROR OCCURRED]: {e}")
