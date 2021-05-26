## How to use:
As of right now, the HTML content of the run must be saved locally. The file path(s) must then be placed in the ```urls``` variable in ```caseid_scraper/caseid_scraper/spiders/caseid_spider.py```

After that you may run the scraper from the current folder:
```bash
pipenv shell
# get caseids of test cases in sections, specified in SECTIONS of caseid_spider.py
scrapy crawl caseid_spider -O scraped_content/caseids.json 
# get caseids of all test cases
scrapy crawl caseid_spider -O scraped_content/caseids.json -a all-sections=True
```
The output will be placed in ```scraped_content/caseids.json```
