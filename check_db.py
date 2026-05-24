from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres123@localhost:5432/marketpulse360')

with engine.connect() as conn:
    print('=== MART_CUSTOMER_VALUE ===')
    r = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='mart_customer_value' AND table_schema='analytics'"))
    for row in r: print(row)

    print('\n=== MART_REVENUE ===')
    r2 = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='mart_revenue' AND table_schema='analytics'"))
    for row in r2: print(row)