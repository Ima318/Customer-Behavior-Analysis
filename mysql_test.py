from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:thariima20030126@localhost/cutomer_behaviour"
)

connection = engine.connect()

print("Connected successfully!")

connection.close()