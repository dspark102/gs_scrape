""" Unit test """

from gs_scrape import gs_scrape

def test_gs_paper_content():
    from gs_scrape import gs_scrape
    a=gs_scrape.GSscraper()
    a._gs_paper_content("machine learning")
    assert a.paperdata is not None

def test_get_citation():
    from gs_scrape import gs_scrape
    a=gs_scrape.GSscraper()
    a._gs_paper_content("machine learning")
    firstid=list(a.paperdata.keys())[0]
    a.get_citation(pid=firstid)
    assert a.papercitation is not None

    