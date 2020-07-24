import requests
from flask import Flask, render_template, Markup

app = Flask(__name__)



@app.route('/home')
def index():
	query = "albert einstein"

	PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": query
	}

	res = requests.get("https://en.wikipedia.org/w/api.php?", 
		params = PARAMS)

	if res.status_code != 200:
	    raise Exception("ERROR: API request unsuccessful.")

	data = res.json()

	data = data["query"]["search"]


	return render_template('index.html', results=data)


if __name__ == '__main__':
	app.run(debug=True)