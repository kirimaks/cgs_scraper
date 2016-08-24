# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import tools


class CglSpider(scrapy.Spider):
    name = "cgl"
    allowed_domains = ["craigslist.org"]
    start_urls = (
        # 'http://www.craigslist.org/about/sites/',
        'http://www.craigslist.org/about/sites/?lang=en&cc=us',
    )
    handle_httpstatus_list = [301, 302, 307]

    def parse(self, response):

        # Select the block with list of us cities.
        us_city_list_xp = "//h1[contains(text(),'US')]/\
following-sibling::div[1]"
        us_city_block = response.xpath(us_city_list_xp)

        # Select links from the block.
        us_city_link_xp = ".//div/ul/li/a/@href"
        links_list = us_city_block.xpath(us_city_link_xp)

        # ##### DEBUG #######
        self.logger.debug("")
        self.logger.debug("<<<<<< LINKS ARRAY BEGIN >>>>>>")
        for link in links_list[:20]:
            link = tools.make_resume_list_link(link)
            self.logger.debug(link)
        self.logger.debug("<<<<<< LINKS ARRAY END >>>>>>\n\n")
        # ##### DEBUG #######

        for link in links_list[:20]:
            link = tools.make_resume_list_link(link)
            yield Request(link,
                          callback=self.parse_resume_list)

    def parse_resume_list(self, response):
        """ Parse resume list of a city """

        self.logger.info("*** Parse page: [{}] ***".format(response.url))
        self.logger.info("\n\n### BODY CONTENT BEGIN ###\n\n {}\
\n\n### BODY CONTENT END ###\n\n".format(response.body))

        title = response.xpath("//title/text()").extract()[0]

        try:
            total_count_xp = "//span[@class='totalcount']/text()"
            resume_number = response.xpath(total_count_xp).extract()[0]
        except IndexError:
            resume_number = 99  # There is less than 100 records.

        links = tools.get_resume_links(response)

        pages = [i * 100 for i in range((int(resume_number) // 100) + 1)]

        yield dict(title=title,
                   url=response.url,
                   count=resume_number,
                   links=links,
                   pages=str(pages))
