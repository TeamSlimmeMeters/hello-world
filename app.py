from flask import Flask

app = Flask(__name__)

@app.route('/Erwin')
def index():
	return '<H1>Lekker Ding</H1>'