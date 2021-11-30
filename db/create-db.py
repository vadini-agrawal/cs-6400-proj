import os
import sqlite3
import pandas as pd
import pdb
# Connect and create cursor
# conn = sqlite3.connect('image.db')
# c = conn.cursor()
# # Create a table 
# c.execute("""
#     CREATE TABLE image_features (
#         id text,
#         feature text,
#         url text
#     )""")
# conn.commit()
# conn.close()
# conn = sqlite3.connect('database_sample.db')

input_root = "csv_10000"
db_path = "database.db"
conn = sqlite3.connect(db_path)


df = pd.read_csv(os.path.join(input_root,"IMAGE.csv"))
df.to_sql("IMAGE", conn, if_exists='replace', index=False)

df = pd.read_csv(os.path.join(input_root,"OBJECT.csv"))
df.to_sql("OBJECT", conn, if_exists='replace', index=False)

df = pd.read_csv(os.path.join(input_root,"IMAGE_OBJECT_DETAILS.csv"))
df.to_sql("IMAGE_OBJECT_DETAILS", conn, if_exists='replace', index=False)

conn.commit()
conn.close()

