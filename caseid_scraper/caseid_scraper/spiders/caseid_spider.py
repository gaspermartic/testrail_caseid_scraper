import scrapy

SPIDER_NAME = 'caseid_spider'
STATUS_STRINGS = [
    'Untested',
    'Retest',
]
# TODO: static right now, add as command line parameter OR json/csv file?
SECTIONS = [
    'SSID and password management',
]

class CaseIdSpider(scrapy.Spider):
    name = SPIDER_NAME

    def start_requests(self):

        # TODO: static right now, add as command line parameter
        urls = [
            'file:///home/gasper/Downloads/htmls/FRV%20AUG%203.4.1-36%20-%20TestRail.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        print('===========')
        result = []
        
        # ids (strings) of all html elements <tr> which contain test case info
        tr_ids = response.xpath('//*/tr[contains(@class, "row odd") or contains(@class, "row even")]/@id').getall()
        for tr_id in tr_ids:
            columns = response.xpath(f'//*/tr[@id="{tr_id}"]/td/a/text()').getall()
            # this works for now: iterate through all columns and if one of them is 'Retest' or 'Untested', push test to list of caseids 
            # TODO: the smarter solution would be scraping the section's first row with column names (only needs to be done once)
            if any(s in columns for s in STATUS_STRINGS):
                case_id = columns[0]
                result.append(case_id)

        result_str = ','.join(result)
        yield {'result': result_str}
        print('===========')
        # remove duplicates!!

        