import wikipediaapi
import requests



class Sections():
	def __init__(self):
		self.pageSections = {}
	
	def generate_sections(self, sections, level=0):
		for s in sections:
			self.pageSections[s.title] = s.text
			Sections.generate_sections(self, s.sections, level+1)

	def pageSectionsText(self):
		return self.pageSections


class Wikipedia():
	def __init__(self, lang):
		self.lang = lang
		self.query = ''
		self.url = "https://en.wikipedia.org/w/api.php?"

	def search(self, query, limit=10):
		self.query = query

		jsonParameters = {
		    "action": "query",
		    "format": "json",
		    "list": "search",
		    "srsearch": self.query
		}

		res = requests.Session().get(self.url, params=jsonParameters)

		if res.status_code != 200:
		    raise Exception("ERROR: API request unsuccessful.")

		data = res.json()
		data = data["query"]["search"]

		result = []
		for item in data:
			result.append(item["title"])


		return result


	def makeRequest(self,query, html=False, lang='default'):
		if html:
			wiki = wikipediaapi.Wikipedia(
					language=self.lang,
					extract_format=wikipediaapi.ExtractFormat.HTML
				)
		else:
			wiki = wikipediaapi.Wikipedia(
					language=self.lang,
					extract_format=wikipediaapi.ExtractFormat.WIKI
				)

		page = wiki.page(query)
		if lang != 'default':
			page = page.langlinks[lang]

		if page.exists():
			leb = Sections()
			leb.generate_sections(sections=page.sections)
			final_result = {
				"title" : page.title,
				"summary" : page.summary,
				"url" : {
					"canonicalurl" : page.canonicalurl,
					"fullurl" : page.fullurl
				},
				"fullSections" : leb.pageSectionsText(),
				"sectionTitles" : leb.pageSectionsText().keys(),
				"pageLanguages" : page.langlinks.keys(),
				"categories" : page.categories
			}	

		else:
			raise Exception("Page not Exists!")

		return final_result


class WolframAlpha():
	def __init__(self):
		self.appID = '9VXTX4-J7ATP4GJPR'
		self.url = 'http://api.wolframalpha.com/v2/query?'

	def makeRequest(self, query):
		jsonParameters = {
			'appid' : self.appID,
			'output' : 'json',
			'input' : query,
			'format' : 'plaintext',
			'translation' : 'true'
		}

		request = requests.Session().get(self.url, params = jsonParameters)
		session = request.json()['queryresult']['pods']

		final_plaintexts = {}

		if request.status_code != 200:
			raise Exception("Error was occured when loading the page.")

		for j in session:
			if len(j['subpods'][0]['plaintext']) != 0:
				final_plaintexts[[j][0]['title']] = j['subpods'][0]['plaintext']


		return final_plaintexts



if __name__ == '__main__':
	pass



