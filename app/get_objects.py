import sqlite3

def get_descriptions(path):
    with sqlite3.connect("../db/database.db") as con:
        cur = con.cursor()
        cur.execute(
            "SELECT IMAGE_OBJECT_DETAILS.action, OBJECT.class_name FROM IMAGE JOIN IMAGE_OBJECT_DETAILS ON IMAGE.image_id = IMAGE_OBJECT_DETAILS.img_id JOIN OBJECT ON IMAGE_OBJECT_DETAILS.object_bb = OBJECT.bb_id WHERE image_path = ? GROUP BY OBJECT.class_name", (path, ))
        rows = cur.fetchall()
        for row in rows:
            if row[0] != "no_interaction":
                temp = row[0].split("_")
                article = "a"
                if row[1][0] in ['a', 'e', 'i','o', 'u']:
                    article = "an"
                if len(temp) == 2:
                    return "person "+temp[0]+"ing "+temp[1]+" "+article+" "+row[1]
                else:
                    if row[0][-1] == "e":
                        return "person "+row[0][0:len(row[0])-1]+"ing "+article+" "+row[1]
                    else:
                        return "person "+row[0]+"ing "+article+" "+row[1]
