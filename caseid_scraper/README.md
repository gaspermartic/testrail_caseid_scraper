## How to use:
As of right now, the HTML content of the run must be saved locally and non-HTML files must be deleted. The file path(s) must then be placed in the ```urls``` variable in ```caseid_scraper/caseid_scraper/spiders/caseid_spider.py```

After that you may run the scraper from the current folder:
```
pipenv shell
scrapy crawl caseid_spider -O scraped-content/caseids.json -a save-files=True 
```
The output will be placed in ```scraped-content/caseids.json```