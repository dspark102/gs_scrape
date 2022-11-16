# required libraries.
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import lxml

class GSscaper():
    
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
        >>>gs=GSscaper() # create an instance

        >>>gs._gs_paper_content(q='samsung')
        {'A-lxPM4d9bQJ': {'title': 'The Influence of Brand Image and Atmosphere Store on Purchase Decision for Samsung Brand Smartphone with Buying Intervention a ....}

        """
        self.params['q']=str(q)
        self.params['as_ylo']=int(year)

        data={}
        while self.params['start']<(maxpage*10):
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
        >>>gs=GSscaper() # create an instance

        >>>gs._gs_paper_content(q='samsung')
        {'A-lxPM4d9bQJ': {'title': 'The Influence of Brand Image and Atmosphere Store on Purchase Decision for Samsung Brand Smartphone with Buying Intervention a ....}
        
        >>>gs.get_citation(pid='A-lxPM4d9bQJ')
        {'A-lxPM4d9bQJ': {'Citation': {'MLA': ...., 'APA':...., 'Chicago':...., 'Harvard': ...., 'Vancouver: ....,}}

        """
        citations={}
        url=f'https://scholar.google.com/scholar?output=cite&q=info:{pid}:scholar.google.com'
        response=requests.get(url, headers=self.headers)
        response
        soup=BeautifulSoup(response.content, 'lxml')
        lists = soup.select('tr')
        citation={}
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
        >>>gs=GSscaper() # create an instance

        >>>gs._gs_paper_content(q='samsung')
        {'A-lxPM4d9bQJ': {'title': 'The Influence of Brand Image and Atmosphere Store on Purchase Decision for Samsung Brand Smartphone with Buying Intervention a ....}
        
        >>>gs.save_csv()

        """
        searchkw=self.params['q'].replace(" ", "_").lower()
        filename=searchkw+".csv"

        df=pd.DataFrame(self.paperdata).T
        df.to_csv(filename)

