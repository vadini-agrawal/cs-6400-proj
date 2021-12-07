import sqlite3

def get_descriptions(path):
    with sqlite3.connect("../db/database.db") as con:
        cur = con.cursor()
        print(path)
        cur.execute(
            "SELECT IMAGE_OBJECT_DETAILS.action, OBJECT.class_name FROM IMAGE JOIN IMAGE_OBJECT_DETAILS ON IMAGE.image_id = IMAGE_OBJECT_DETAILS.img_id JOIN OBJECT ON IMAGE_OBJECT_DETAILS.object_bb = OBJECT.bb_id WHERE image_path = ? GROUP BY OBJECT.class_name", (path, ))
        rows = cur.fetchall()
        for row in rows:
            if row[0] != "no_interaction":
                return "The image has a person "+row[0]+"ing a "+row[1]
