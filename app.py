from flask import Flask, render_template

app = Flask(__name__)

tasks = [
    {'name': 'Estudar', 'finished': False},
    {'name': 'Dormir', 'finished': True},
    {'name': 'Comer', 'finished': True},
    {'name': 'Travazap pra Lucimeire', 'finished': False}
]

@app.route("/")
def home():
    # templates/home.html
    return render_template('home.html', tasks=tasks)

@app.route("/bye")
def bye():
    return 'Bye!'

app.run(debug = True)
