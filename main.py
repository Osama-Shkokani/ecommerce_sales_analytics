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

print("\n __After Cleaning__")
print(f"Total Rows: {len(df)}")
print(df.info())

