## How to use:
As of right now, the HTML content of the run must be saved locally. The ```.html``` file must then be placed in ```caseid_scraper/caseid_scraper/thml_testrail_runs```.

After that you may run the scraper from the current folder by running the following commands and changing ```FILE NAME.html``` to the name of your saved file:
```bash
pipenv shell
# get caseids of test cases in sections, specified in SECTIONS of caseid_spider.py
scrapy crawl caseid_spider -O scraped_content/caseids.json -a file-name="<FILE NAME.html>"
# get caseids of all test cases
scrapy crawl caseid_spider -O scraped_content/caseids.json -a all-sections=True -a file-name="<FILE NAME.html>"
```
The output will be placed in ```scraped_content/caseids.json```.

### Tips & Tricks
Append the following lines to your ```~/.bashrc``` file and change ```<FULL-PATH-TO-REPOSITORY>``` to the path of the repository on your system.
```bash
scrapesection() {
        if [ $# -eq 0 ]
                then
                        echo "You need to pass the .html file name as an argument to this command for it to work"
                        return
        fi
        cd <FULL-PATH-TO-REPOSITORY>/caseid_scraper ;
        pipenv run scrapy crawl caseid_spider -O caseid_scraper/scraped_content/caseids.json -a file-name="$1";
        cd -
}

scrapeall() {
        if [ $# -eq 0 ]
                then
                        echo "You need to pass the .html file name as an argument to this command for it to work"
                        return
        fi
        cd <FULL-PATH-TO-REPOSITORY>/caseid_scraper ;
        pipenv run scrapy crawl caseid_spider -O caseid_scraper/scraped_content/caseids.json -a all-sections=True -a file-name="$1";
        cd -
}
```
Then you can easily run:
```bash
scrapesection 'FILE NAME.html'
scrapeall 'FILE NAME.html'
```
from anywhere in your terminal.