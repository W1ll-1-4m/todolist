from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, web"

@app.route("/bye")
def bye():
    return "bye"

app.run(debug = True)