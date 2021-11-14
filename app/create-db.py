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
conn = sqlite3.connect('database_sample.db')
df = pd.read_csv("../db/IMAGE.csv")
df.to_sql("IMAGE", conn, if_exists='replace', index=False)

df = pd.read_csv("../db/OBJECT.csv")
df.to_sql("OBJECT", conn, if_exists='replace', index=False)

df = pd.read_csv("../db/IMAGE_OBJECT_DETAILS.csv")
df.to_sql("IMAGE_OBJECT_DETAILS", conn, if_exists='replace', index=False)
conn.commit()
conn.close()

