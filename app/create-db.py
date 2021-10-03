import sqlite3

# Connect and create cursor
conn = sqlite3.connect('image.db')
c = conn.cursor()

# Create a table 
c.execute("""
    CREATE TABLE image_features (
        id text,
        feature text,
        url text
    )""")
conn.commit()
conn.close()