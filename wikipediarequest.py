import requests


class Wikipedia:
	def __init__(self):
		 pass



	def search(self, query, limit=10, lang='en'):
		jsonParameters = {
		    "action": "query",
		    "format": "json",
		    "list": "search",
		    "srsearch": query
		}

		res = requests.Session().get("https://en.wikipedia.org/w/api.php?", params=jsonParameters)

		if res.status_code != 200:
		    raise Exception("ERROR: API request unsuccessful.")

		data = res.json()
		data = data["query"]["search"]


		result = []
		for item in data:
			result.append(item["title"])

		return result



def test():

	S = requests.Session()

	URL = "https://test.wikipedia.org/w/api.php"

	# Step 1: GET request to fetch login token
	PARAMS_0 = {
	    "action": "query",
	    "meta": "tokens",
	    "type": "login",
	    "format": "json"
	}

	R = S.get(url=URL, params=PARAMS_0)
	DATA = R.json()

	LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

	# Step 2: POST request to log in. Use of main account for login is not
	# supported. Obtain credentials via Special:BotPasswords
	# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
	PARAMS_1 = {
	    "action": "login",
	    "lgname": "bot_user_name",
	    "lgpassword": "bot_password",
	    "lgtoken": LOGIN_TOKEN,
	    "format": "json"
	}

	R = S.post(URL, data=PARAMS_1)

	# Step 3: GET request to fetch CSRF token
	PARAMS_2 = {
	    "action": "query",
	    "meta": "tokens",
	    "format": "json"
	}

	R = S.get(url=URL, params=PARAMS_2)
	DATA = R.json()

	CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

	# Step 4: POST request to change page language
	PARAMS_3 = {
	    "action": "setpagelanguage",
	    "pageid": "123",
	    "token": CSRF_TOKEN,
	    "format": "json",
	    "lang": "eu"
	}

	R = S.post(URL, data=PARAMS_3)
	DATA = R.json()

	print(DATA)


if __name__ == '__main__':
	print(Wikipedia().search(query="isaac newton"))