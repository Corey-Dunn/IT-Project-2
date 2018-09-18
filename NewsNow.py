import requests
from bs4 import BeautifulSoup


class NewsNowScraper:

    # Class constructor: Initialises the keyword and page URL.
    def __init__(self, term):
        self.term = term  # Keyword
        self.url = "http://www.newsnow.co.uk/h/?search={0}&lang=en".format(self.term)  # URL

    def run(self):
        response = requests.get(self.url)
        # Generate a 'soup', with all the HTML code from the website.
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all the div's with the class 'hl_inner' which specifies that it is a headline on the page.
        headline_results = soup.find_all('div', class_='hl__inner')
        # Iterate through the headlines, pulling out key data.
        values = []
        for h in headline_results:
            # Find the headline within the HTML.
            content = h.find('a', class_='hll').getText()
            try:
                # Find the story's source.
                src = h.find('span', class_='src').getText()
                # print("Source: ", src)
            except AttributeError:
                src = "NewsNow"
                # print("Source: ", src)
            # Find the story's Timestamp.
            time = h.find('span', class_='time').getText()
            # print("Time: ", time)
            # Find the link (story URL).
            link = h.find('a').get('href')
            # print("Link: ", link)
            # print("Content: ", content)
            values.append((src, content, time, link, self.term))
        print("NewsNow - Term: ", self.term)
        # Print the number of stories found that relate to the keyword.
        print("Results: ", len(headline_results))
        return values


