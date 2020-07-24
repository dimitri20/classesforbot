import wikipediaapi


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
	def __init__(self, lang, query):
		self.lang = lang
		self.query = query


	def result(self, html=False, lang='default'):
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

		page = wiki.page(self.query)
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




if __name__ == '__main__':
	obj = Wikipedia(query="Albert Einstein", lang='en') 
	print(obj.result()["sectionTitles"])
	inp = input("Enter title")
	print(obj.result()["fullSections"][inp])



