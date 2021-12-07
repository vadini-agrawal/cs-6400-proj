import os 

from flask import Flask, render_template, request
from parse_query import parse_sentence 
from append_image import get_similar_images
from get_objects import get_descriptions
import sqlite3
import pdb

# Create Flask's `app` object
app = Flask(
    __name__,
    template_folder="templates"
)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/sentence-query", methods=['POST'])
def sentence_query():
    if request.method == 'POST':
        result = request.form
        result = result['query']
        print(result)
        actions, objects = parse_sentence(result)
        print(actions,objects)

        filenames = []
        for action in actions:
            for object in objects:
                with sqlite3.connect("../db/database.db") as con:
                    cur = con.cursor()
                    cur.execute("select image_path from IMAGE i join IMAGE_OBJECT_DETAILS iod join OBJECT o where i.image_id = iod.img_id and o.bb_id = iod.object_bb and class_name = ? and action = ?",(object, action))
                    rows = cur.fetchall();
                    for url in rows:
                        if url[0][3:] not in filenames:
                            filenames.append(url[0][3:])
        
        
        return render_template("index.html",result=result, filenames=filenames)

@app.route("/image-query", methods=['POST'])
def image_query():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "no file"
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join('static', filename))
            # use saved image to query here
            filenames = get_similar_images('static/'+filename)
            description = get_descriptions(filenames[0])
            return render_template('index2.html', filenames=filenames, description=description)
        else:
            return "File uploaded is not a valid image"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = "127.0.0.1", port = 5000, debug=True)