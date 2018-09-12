import requests
from bs4 import BeautifulSoup


class ThreatPostScraper:

    # Class constructor: Initialises the keyword and page URL.
    def __init__(self, term):
        self.term = term  # Keyword
        self.url = "https://threatpost.com/?s={}".format(self.term)  # URL
        self.src = "ThreatPost"  # source

    def run(self):
        response = requests.get(self.url)
        # Generate a 'soup', with all the HTML code from the website.
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the div's with the class 'hl_inner' which specifies that it is a headline on the page.
        headline_results = soup.find_all('article', class_='c-card c-card--horizontal--half@md '
                                                           'c-card--horizontal@lg '
                                                           'c-card--horizontal--flat@md')

        # Iterate through the headlines, pulling out key data.
        values = []
        for h in headline_results:
            # Find the title within the HTML.
            title = h.find('h2', class_='c-card__title').find('a').getText().strip()
            # Find the stories description
            desc = h.find('div', class_='o-col-12@md o-col-4@lg c-card__col-desc').getText().strip()
            # Find the stories author
            author = h.find('div', class_='c-card__author').getText().strip()
            # Find the story's Timestamp.
            time = h.find('div', class_='c-card__time').getText().strip()
            # Find the link (story URL).
            link = h.find('h2', class_='c-card__title').find('a').get('href')
            # append vaules list
            values.append((self.src, title, desc, author, time, link, self.term))
        print("Term: ", self.term)
        # Print the number of stories found that relate to the keyword.
        print("Results: ", len(headline_results))
        print(values)

        return values


x = ThreatPostScraper("exploit")
x.run()
