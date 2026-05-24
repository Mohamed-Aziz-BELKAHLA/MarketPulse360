import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Charger tous les CSV
tables = {
    "raw_customers":    "data/raw/olist_customers_dataset.csv",
    "raw_orders":       "data/raw/olist_orders_dataset.csv",
    "raw_order_items":  "data/raw/olist_order_items_dataset.csv",
    "raw_payments":     "data/raw/olist_order_payments_dataset.csv",
    "raw_products":     "data/raw/olist_products_dataset.csv",
    "raw_sellers":      "data/raw/olist_sellers_dataset.csv",
    "raw_reviews":      "data/raw/olist_order_reviews_dataset.csv",
    "raw_category_translation": "data/raw/product_category_name_translation.csv",
}

for table_name, filepath in tables.items():
    df = pd.read_csv(filepath)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ {table_name} chargé — {len(df)} lignes")

print("\n🎉 Toutes les données sont dans PostgreSQL !")