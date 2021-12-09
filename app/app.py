import os 

from flask import Flask, render_template, request
from parse_query import parse_sentence 
from append_image import get_similar_images, load_features, extract_feature, compute_closest
from get_objects import get_descriptions
import sqlite3
import random
import pdb
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# Create Flask's `app` object
app = Flask(
    __name__,
    template_folder="templates"
)

feat_normed, imlist = load_features()

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
        print("Query :",result)
        actions, objects = parse_sentence(result)
        if 'person' in objects:
            objects.remove('person')
        print("Actions :",actions)
        print("Objects :",objects)

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
        templ = len(filenames)
        if len(filenames)!=0:
            random.shuffle(filenames)
        
        tokenized = nltk.word_tokenize(result)
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN')]
        verbs = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:1] == 'V')]
        if 'person' in nouns:
            nouns.remove('person')
        if 'people' in nouns:
            nouns.remove('people')

        if len(filenames) == 0:
            for action in actions:
                with sqlite3.connect("../db/database.db") as con:
                    cur = con.cursor()
                    cur.execute("select image_path from IMAGE i join IMAGE_OBJECT_DETAILS iod join OBJECT o where i.image_id = iod.img_id and o.bb_id = iod.object_bb and action = ? LIMIT 100",(action,))
                    rows = cur.fetchall();
                    for url in rows:
                        if url[0][3:] not in filenames:
                            filenames.append(url[0][3:])

            for object in objects:
                with sqlite3.connect("../db/database.db") as con:
                    cur = con.cursor()
                    cur.execute("select image_path from IMAGE i join IMAGE_OBJECT_DETAILS iod join OBJECT o where i.image_id = iod.img_id and o.bb_id = iod.object_bb and class_name = ? LIMIT 100",(object,))
                    rows = cur.fetchall();
                    for url in rows:
                        if url[0][3:] not in filenames:
                            filenames.append(url[0][3:])
        flag = 0
        if len(nouns)!=0 and len(verbs)!=0 and templ==0 and len(filenames)!=0:
            result = "No results found for '" + result +"' Showing related images"
            flag = 1
        if flag == 1:
            random.shuffle(filenames)
            flag = 0
        if len(filenames) == 0 and flag==0:
            result = "No results found for '" + result + "'"
        return render_template("index.html",result=result, filenames=filenames[0:100])

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
            feat = extract_feature('static/'+filename)
            filenames = compute_closest(feat_normed, imlist, feat, topk=10)
            # filenames = get_similar_images('static/'+filename)
            descriptions = []
            for i in filenames:
                descriptions.append(get_descriptions(".."+i[6:]))
            l = len(filenames)
            return render_template('index2.html', your_image='static/'+filename, filenames=filenames[0:100], descriptions=descriptions, l=l)
        else:
            return "File uploaded is not a valid image"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = "127.0.0.1", port = 5000, debug=True)