# gs_scrape

Extract Google Scholar search results.

gs_scrape is a customized GoogleScholar research results scraping tool. You can extract any publications with user's own 'key words', 'year of publication', 'number of pages'.

All publication's information such as publication id (used in GoogleScholar), title, author(s), digital document location, numbers of being cited are stored. 

Using the publication ids, you can further extract the useful (different) types of citation format. Basically GoogleScholar provides five differnt citation format (e.g., APA, Chicago, Harvard and so on). Extract and download the citations are super useful and time-saving method in particular for those who are instantaly save the right form of citation. You can save the data in .csv file. 

Lastly, citation_graph method provide horizontal bar chart to visually check which publications are most citied so far. 



## Installation

```bash
$ pip install gs_scrape
```

## Usage

- vignette.ipynb file is provided as an example

- https://gs-scrape.readthedocs.io/en/latest/

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`gs_scrape` was created by Baek Park. It is licensed under the terms of the MIT license.

## Credits

`gs_scrape` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
