from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("index.html", name='Jose')

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/name")
def get_name():
    return "Jose"

if __name__ == "__main__":
    app.run()
