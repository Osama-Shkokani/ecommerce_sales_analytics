import pandas as pd
from database import DatabaseManager

class ECommerceAnalytics(DatabaseManager) :
    """A class to handle all analytical queries for E-Commerce sales."""

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
    
    def get_top_spenders(self, limit=5):
        self.connect()

        query =f"""
                SELECT t.CustomerID ,SUM(t.Quantity * t.UnitPrice) as TotalSpent
                FROM transactions t 
                WHERE CustomerID IS NOT NULL
                GROUP BY t.CustomerID
                ORDER BY TotalSpent DESC
                LIMIT {limit};
        """
        result_df = pd.read_sql_query(query, self.conn)
        self.close()
        return result_df
