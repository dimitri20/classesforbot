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




"""

def print_langlinks(page):
        langlinks = page.langlinks
        for k in sorted(langlinks.keys()):
            v = langlinks[k]
            print("%s: %s - %s: %s" % (k, v.language, v.title, v.fullurl))

print_langlinks(page_py)
# af: af - Python (programmeertaal): https://af.wikipedia.org/wiki/Python_(programmeertaal)
# als: als - Python (Programmiersprache): https://als.wikipedia.org/wiki/Python_(Programmiersprache)
# an: an - Python: https://an.wikipedia.org/wiki/Python
# ar: ar - بايثون: https://ar.wikipedia.org/wiki/%D8%A8%D8%A7%D9%8A%D8%AB%D9%88%D9%86
# as: as - পাইথন: https://as.wikipedia.org/wiki/%E0%A6%AA%E0%A6%BE%E0%A6%87%E0%A6%A5%E0%A6%A8

page_py_cs = page_py.langlinks['cs']
print("Page - Summary: %s" % page_py_cs.summary[0:60])
# Page - Summary: Python (anglická výslovnost [ˈpaiθtən]) je vysokoúrovňový sk


"""