# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import tools.select_tools as tools

from urllib.parse import urljoin

from subprocess import Popen, PIPE
import json

from multiprocessing import Pool


def start_casper(url):
    p = Popen(['casperjs', 'casper/parse_resume.js',
               '--url={}'.format(url)], stdout=PIPE)
    p.wait()
    resp = p.stdout.read().decode('utf-8')
    resp = json.loads(resp)
    return resp


class CglSpider(scrapy.Spider):
    name = "cgl"
    allowed_domains = ["craigslist.org"]
    start_urls = (
        # 'http://www.craigslist.org/about/sites/',
        'http://www.craigslist.org/about/sites/?lang=en&cc=us',
    )
    # handle_httpstatus_list = [301, 302, 307]

    def parse(self, response):

        # Select the block with list of us cities.
        us_city_list_xp = "//h1[contains(text(),'US')]/\
following-sibling::div[1]"
        us_city_block = response.xpath(us_city_list_xp)

        # Select links from the block.
        us_city_link_xp = ".//div/ul/li/a/@href"
        links_list = us_city_block.xpath(us_city_link_xp)

        for link in links_list:
            link = tools.make_resume_list_link(link)
            yield Request(link, callback=self.parse_pagination)

    def parse_pagination(self, response):
        self.logger.info("*** Parse page: [{}] ***".format(response.url))

        try:
            total_count_xp = "//span[@class='totalcount']/text()"
            resume_number = response.xpath(total_count_xp).extract()[0]
        except IndexError:
            resume_number = 99  # There is less than 100 records.

        pagination = [i * 100 for i in range((int(resume_number) // 100) + 1)]

        for page in pagination:
            url = urljoin(response.url, "?s={}".format(page))
            yield Request(url, callback=self.parse_resume_list)

    def parse_resume_list(self, response):
        self.logger.info("*** Parse page: [{}] ***".format(response.url))
        resume_urls = tools.get_resume_links(response)

        pool = Pool(4)
        jobs = [pool.apply_async(start_casper, [url]) for url in resume_urls]
        pool.close()

        for job in jobs:
            yield job.get()
