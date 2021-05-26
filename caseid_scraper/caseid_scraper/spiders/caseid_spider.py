import scrapy

SPIDER_NAME = 'caseid_spider'
STATUS_STRINGS = [
    'Untested',
    'Retest',
]
# TODO: static right now, add as command line parameter OR json/csv file?
# all sections are scraped if the all-sections option is passed (-a all-sections=True)
SECTIONS = [
    # 'OpenSync Steering',
    # 'Client Steering',
    # 'Optimization',
    # 'DFS',
    # 'VSB',
    # 'IPv6',
    # 'M2U, IGMP Snooping and IGMP Proxy',
    # 'IGMP',
    # 'Networking',
    # 'HomePass',
    # 'Wired clients',
    # 'Security',
    # 'Platform',
]

class CaseIdSpider(scrapy.Spider):
    name = SPIDER_NAME

    def start_requests(self):
        self.all_sections = False
        if getattr(self, 'all-sections', None) == 'True':
            self.all_sections = True

        # TODO: static right now, add as command line parameter
        # TODO: add support for multiple urls (yield results with different names)
        urls = [
            'file:///home/gasper/Downloads/htmls/FRV%20AUG%203.4.1-36%20-%20TestRail.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        result = None
        if (self.all_sections):
            result = self.get_all_caseids(response)
        else:
            result = self.get_sections_caseids(response)


        result_str = ','.join(result)
        print(f'\nNumber of scraped cases: {len(result)}\n')
        yield {'result': result_str}
    
    def get_all_caseids(self, response):
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

        return result

    def get_sections_caseids(self, response):
        result = []

        for section in SECTIONS:
            result += self.get_section_caseids(response, section)

        return result

    def get_section_caseids(self, response, section):
        result = []
        # id (string) of html element <div> which contains all <tr> of test cases in desired section
        # the section is a <span> which contains section text and classes 'title pull-left', cases are contained in its 2nd ancestor div
        section_id = response.xpath(f'//*/span[contains(text(), "{section}") and contains(@class, "title pull-left")]/ancestor::div[2]/@id').getall()[0]
        # ids (strings) of all html elements <tr> which contain test case info and are in section section_id
        tr_ids = response.xpath(f'//*[@id="{section_id}"]//*/tr[contains(@class, "row odd") or contains(@class, "row even")]/@id').getall()
        for tr_id in tr_ids:
            columns = response.xpath(f'//*/tr[@id="{tr_id}"]/td/a/text()').getall()
            if any(s in columns for s in STATUS_STRINGS):
                case_id = columns[0]
                result.append(case_id)
        return result

# TODO: add check if test is Automated