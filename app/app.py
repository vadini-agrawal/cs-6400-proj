from flask import Flask, render_template, request

# Create Flask's `app` object
app = Flask(
    __name__,
    template_folder="templates"
)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/get-button", methods=['POST'])
def show_text():
    if request.method == 'POST':
      result = request.form
      result = result['general']
      return render_template("index.html",result=result)

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000)