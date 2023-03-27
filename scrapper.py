import regex as re # provides regular expression matching operations
import requests # simple, yet elegant, HTTP library
from bs4 import BeautifulSoup as bs # library for pulling data out of HTML and XML files

class Scraper:
    """
    A Web Scrapper Class whose object can be instantiated
    in order to scrap the tremding and latest
    academic research papers related to AI from
    the paperwithcode.com website
    """
    def __init__(self):
        self.rootURL = 'https://paperswithcode.com'
        self.trendingPapersURL = self.rootURL
        self.latestURL = 'https://paperswithcode.com/latest'
        self.linkToPaperPage = None
        self.trendingPapers = None
        self.latestPapers = None

    # scraps the trending papers
    def scrapTrending(self):
        req = requests.get(self.trendingPapersURL) # a request to get the trending papers based on the url
        soup = bs(req.text, 'lxml') # stores the beautifulsoup object and parses with xml 
        
        self.trendingPapers = self.scrapPage(soup) # gets final scrapped data related to trending papers

        return self.trendingPapers

    # scraps the latest papers
    def scrapLatest(self):
        req = requests.get(self.latestURL) # a request to get the latest papers based on the url
        soup = bs(req.text, 'lxml') # stores the beautifulsoup object and parses with xml 

        self.latestPapers = self.scrapPage(soup).copy() # gets final scrapped data related to latest papers

        return self.latestPapers


    def scrapPage(self, soup):
        papers_dict = {} # a dictionary to hold the key-value pairs related to the papers
        papers = [] # a list of all scrapped paper dictionaries

        items_divs = soup.find_all('div', {'class':'row infinite-item item paper-card'}) # finds all the divs having a class 'row infinite-item item paper-card'

        for item in items_divs: #iterating through the different divs collected in the above step
            for child in item.children: # iterating through the div children
                # Image extraction
                try:
                    # Check if classes are in child attributes
                    if set(child.attrs['class']) <= set(['col-lg-3', 'item-image-col']):
                        # Image url
                        #print(child.find('div', {'class':'item-image'})['style'])  
                        papers_dict['image'] = self.rootURL + str(child.find('div', {'class':'item-image'})['style'].split("('", 1)[1].split("')")[0])
                        #print(papers_dict['image'])
                except:
                    pass

                # Content extraction
                try:
                    if set(child.attrs['class']) <= set(['col-lg-9', 'item-col']):
                        # Title
                        print(child.find('h1').a.string)
                        papers_dict['title'] = child.find('h1').a.string # storing the paper title
                        # Nb stars
                        #print(child.find('span', {'class':'badge badge-secondary'}).text.strip())
                        papers_dict['nb_stars'] = child.find('span', {'class':'badge badge-secondary'}).text.strip() # storing the nb stars received by the paper
                        # Star/hour
                        #print(child.find('div', {'class':'stars-accumulated text-center'}).text.strip())
                        papers_dict['hourly_stars'] = child.find('div', {'class':'stars-accumulated text-center'}).text.strip() # storing the hourly stars received by the paper
                        # Paper page link
                        #print(child.find('a', {'class':'badge badge-light'})['href'])
                        linkToPaperPage = child.find('a', {'class':'badge badge-light'})['href'] # gets the link to the paper
                except:
                    pass

            if linkToPaperPage != None: # checks if link to paper exists
                req = requests.get(self.rootURL + linkToPaperPage) # makes request to the paper link
                linkToPaperPage = None # resets the paper link variable
                soup = bs(req.text, 'lxml') 
                pdf_link = soup.find('a', {'class':'badge badge-light'})['href'] # gets the link to the paper pdf format
                # Check if the link found is the pdf or a search query
                url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
                if re.match(url_pattern, pdf_link) != None: # returns match object
                    r = requests.get(pdf_link)
                else:
                    r = requests.get(self.rootURL + pdf_link)
                
                content_type = r.headers.get('content-type') # gets the content-type from the headers

                if 'application/pdf' in content_type: # checks if the content-type is pdf
                    papers_dict['pdf'] = pdf_link # stores the pdf link of paper
                    # Github link
                    #print(soup.find('a', {'class':'code-table-link'})['href'])
                    papers_dict['github'] = soup.find('a', {'class':'code-table-link'})['href'] # stores the githubb link of paper
                elif 'text/html' in content_type: # checks if the content-type is html
                    soup = bs(r.text, 'lxml')
                    # PDF link
                    #print(soup.find('a', {'class':'badge badge-light'})['href'])
                    papers_dict['pdf'] = soup.find('a', {'class':'badge badge-light'})['href'] # stores the pdf link of paper
                    # Github link
                    #print(soup.find('a', {'class':'code-table-link'})['href'])
                    papers_dict['github'] = soup.find('a', {'class':'code-table-link'})['href'] # stores the githubb link of paper
                # Abstract
                papers_dict['abstract'] = soup.select_one('.paper-abstract p').text.strip() # stores the abstract of the paper
            papers.append(papers_dict.copy()) # stores the paper dictionary in the list
        return papers