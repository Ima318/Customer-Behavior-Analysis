import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("customer_shopping_behavior.csv")

print(df)

# Analyze the data

df.info()
df.describe()

df.isnull().sum()

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()

df.groupby('Category')['Review Rating'].apply(lambda x: x.isnull().sum())

print(df['Review Rating'].dtype)



# Check data type
print("Data type:", df['Review Rating'].dtype)

# Convert to numeric if needed
df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors='coerce')

# Null values before filling
print("\nNulls before:", df['Review Rating'].isnull().sum())

# Fill missing values with category median
df['Review Rating'] = (
    df.groupby('Category')['Review Rating']
      .transform(lambda x: x.fillna(x.median()))
)

# Fill any remaining nulls with overall median
df['Review Rating'] = df['Review Rating'].fillna(
    df['Review Rating'].median()
)

# Null values after filling
print("Nulls after:", df['Review Rating'].isnull().sum())

# Verify
print("\nRemaining nulls by category:")
print(
    df.groupby('Category')['Review Rating']
      .apply(lambda x: x.isnull().sum())
)

df.isnull().sum()

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

print(df.columns)

df.rename(columns= {'purchase_amount(usd)': 'purchase_amount'})

print(df.columns)

#create a new column
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

print(df[['age', 'age_group']].head(10))


#create column purchase frequesncy rate
frequency_mapping= {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quaterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90

}
df['purchase_frequency_rate'] = df['frequency_of_purchases'].map(frequency_mapping)

print(df[['frequency_of_purchases', 'purchase_frequency_rate']].head(10))

print(df[['discount_applied','promo_code_used']].head(10))

(df['discount_applied'] == df['promo_code_used']).all()
#both coulmn carry same information so data is redundant theres for we gonna drop a one coulmn

df.drop('promo_code_used', axis=1, inplace=True)

print(df.columns)

username = "root"
password = "thariima20030126"
host = "localhost"
port="3306"
database = "customer_behaviour"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

table_name = "customer_data"
df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data inserted into MySQL table '{table_name}' successfully!")





