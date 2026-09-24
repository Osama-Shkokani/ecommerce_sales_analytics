import sqlite3
import pandas as pd 

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