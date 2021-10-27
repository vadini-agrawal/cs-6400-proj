from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

import parse_query


# Create Flask's `app` object
app = Flask(
    __name__,
    template_folder="templates"
)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/sentence-query", methods=['POST'])
def sentence_query():
    if request.method == 'POST':
        result = request.form
        result = result['query']
        filenames = ['apple1.jpeg', 'apple2.jpeg', 'apple3.jpeg']
        return render_template("index.html",result=result, filenames=filenames)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = "127.0.0.1", port = 5000)