# required libraries.
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import lxml
import time
import random
import matplotlib.pyplot as plt
import numpy as np


class GSscraper():
    
    def __init__(self):
        self.params={'q':'machine', 'as_ylo':2021, 'hl':'en', 'start':0} 
        # Default values for google scholar searching parameters 
        ## 'q' : query parameter, 'as_ylo" : year of publication at least, "start" : the parameter of page numbe (0: 1st page, 10; 2md page)
        self.headers = {'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        # Header information
        self.paperdata=None
        self.papercitation=None

    def _gs_paper_content(self, q="machine learning", year=2021, maxpage=2):
        """
        Extract paper's information including the number of being cited.

        

        Parameters
        ----------

        q : search query (e.g., "machine learing", "causal model", and so on)
        
        year : the year of publication at leat (if you prefer the latest research papers, please set the nearest years.) 
        
        maxpage : number of resulting pages you want to extrat. Each page has ten articles(or references).


        
        Returns
        --------
        _gs_paper_content() method returns paper's information data in a python dictioonnary format. 

        It includes title, author, document link, and number of being cited for each paper. 

        {'publication id': {'title' : the title of the paper, 'author': author(s) of the paper, 'access': document link, 'numCited': number of being cited}}


        Examples
        ---------
        >>>from gs_scrape import gs_scrape

        >>>gs=gs_scrape.GSscaper() # create an instance

        >>>gs._gs_paper_content(q='samsung')
        {'A-lxPM4d9bQJ': {'title': 'The Influence of Brand Image and Atmosphere Store on Purchase Decision for Samsung Brand Smartphone with Buying Intervention a ....}

        """
        self.params['q']=str(q)
        self.params['as_ylo']=int(year)

        data={}
        while self.params['start']<(maxpage*10):
            time.sleep(random.randint(1,10))
            response=requests.get('https://scholar.google.com/scholar', headers=self.headers, params=self.params)
            print(response)
            soup=BeautifulSoup(response.content, 'lxml')
            lists = soup.select('.gs_ri')
            for list in lists: # looping for each paper (or any other reference)
                title=list.select('h3')[0].get_text() # title informtion
                author=list.select('.gs_a')[0].get_text() # author information (including publisher and publication year)
                link=list.select('a')[0]['href'] # possible electic document links (either html or pdf)
                pid=list.select('[id]')[0]['id'] # publication id 
                others=list.select('div.gs_fl')[0].get_text() # other trivial information 
                pa=re.compile(r"Cited by+\s+[0-9]*") # regular expression is used to locate the number of being cited. 
                try:
                    numCited="".join(pa.findall(others)).split()[-1] # number of being cited. 
                except:
                    numCited=0
                data.update({pid: {'title': title, 'author(s)': author, 'access' : link, 'numCited': numCited}})  

            # next page until the max-page
            if soup.select('.gs_ico_nav_next'):
                self.params['start']+=10
            else:
                break

        self.paperdata=data
        return data


    def get_citation(self,pid):
        """
        Extract the paper's citation reference for a single paper (too many trials might end up with being blocked.)

        Parameter 
        ---------
        pid: publication id (pids are generated and store in self.paperdata).

        
        Returns
        --------
        get_citation() methods provides citation references in different ciation format. The data is stored in dictionary format. 


        Example
        --------
        >>>from gs_scrape import gs_scrape

        >>>gs=gs_scrape.GSscaper() # create an instance

        >>>gs._gs_paper_content(q='samsung')
        {'A-lxPM4d9bQJ': {'title': 'The Influence of Brand Image and Atmosphere Store on Purchase Decision for Samsung Brand Smartphone with Buying Intervention a ....}
        
        >>>gs.get_citation(pid='A-lxPM4d9bQJ')
        {'A-lxPM4d9bQJ': {'Citation': {'MLA': ...., 'APA':...., 'Chicago':...., 'Harvard': ...., 'Vancouver: ....,}}

        """
        citations={} # empty dictionary for citations
        url=f'https://scholar.google.com/scholar?output=cite&q=info:{pid}:scholar.google.com' # url for the citations of specific paper
        response=requests.get(url, headers=self.headers) # request html page
        response # check the response code (expecting 200)
        soup=BeautifulSoup(response.content, 'lxml') # rearrange with Beautiful soup
        lists = soup.select('tr') 
        citation={} # empty dictionary for a single type of citation
        for list in lists:
            ins=list.select('th')[0].get_text()
            cit=list.select('.gs_citr')[0].get_text()
            citation.update({ins:cit})
        citations[id]=({'Citation':citation})
        
        self.papercitation=citations
        return citations 


    def save_csv(self):
        """
        Write in a csv file (save the file in the current working directory)
        The file name is automatically created from 'query kewword'.

        Returns
        -------
        save_csv() method transform the paperdata dictionary into a DataFrame object and store it into .csv file in the current working directory. 
        Filename is 'query'.csv 

        Example
        -------
        >>>from gs_scrape import gs_scrape

        >>>gs=gs_scrape.GSscaper() # create an instance

        >>>gs._gs_paper_content(q='samsung')
        {'A-lxPM4d9bQJ': {'title': 'The Influence of Brand Image and Atmosphere Store on Purchase Decision for Samsung Brand Smartphone with Buying Intervention a ....}
        
        >>>gs.save_csv()

        """
        searchkw=self.params['q'].replace(" ", "_").lower() # replace blank in search query to '-'.
        filename=searchkw+".csv" # create a filename as .csv

        df=pd.DataFrame(self.paperdata).T # transform the paperdata list to pandas' data frame.
        df.to_csv(filename) # save the dataframe as .csv format with the search query name


    def citation_graph(self):

        """
        Create a bar graph of number of being ciated by a paper (or any types of document) after you extract the paper data using 
        key 'query' from the  _gs_paper_content() method.

        Returns
        -------
        citation_graph() method provide a horizontal bar graphs.  

        Example
        -------

        >>>from gs_scrape import gs_scrape
           
        >>>gs=gs_scrape.GSscraper() # create an instance

        >>>gs._gs_paper_content(q='machine learning')
        
        >>>gs.citation_graph()

        """

        info=self.paperdata # read paperdata from the class
        df=pd.DataFrame(info).T # transpose the data frame
        df['numCited']=df['numCited'].apply(int) # change 'numCited' data into integel type.
        y_pos=np.arange(len(df['numCited'])) # y position labels 
        titlename=[" ".join(a.split(" ")[0:5])+"..." for a in df['title']] # paper tile names list
        plt.barh(y_pos,df['numCited'] ) # horizontal bar plot with 'numCited' column data
        plt.subplots_adjust(left=0.6) # modify the left margin so that we can see the paper title as much as possible.
        plt.yticks(y_pos, titlename) # pass the titlename into y ticks.
        plt.show() # show the bar plot 



