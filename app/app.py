import os 

from flask import Flask, render_template, request
from parse_query import parse_sentence 
import sqlite3

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
        actions, objects = parse_sentence(result)
        print(actions,objects)

        filenames = []
        for action in actions:
            for object in objects:
                with sqlite3.connect("database_sample.db") as con:
                    cur = con.cursor()
                    cur.execute("select image_path from IMAGE i join IMAGE_OBJECT_DETAILS iod join OBJECT o where i.image_id = iod.img_id and o.bb_id = iod.object_bb and class_name = ? and action = ?",(object, action))
                    rows = cur.fetchall();
                    for url in rows:
                        filenames.append(url[0])
        return render_template("index.html",result=result, filenames=filenames)

@app.route("/image-query", methods=['POST'])
def image_query():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "no files"
        file = request.files['file']
        if file.filename == '':
            return "no file"
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join('static', filename))
            # use saved image to query here
            return render_template('index.html', filenames=[filename])
        else:
            return "File uploaded is not a valid image"


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = "127.0.0.1", port = 5000, debug=True)