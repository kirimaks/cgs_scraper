from urllib.parse import urljoin
import re

from faker import Factory

faker = Factory().create()


def make_resume_list_link(link):
    link = link.extract()
    link = "http:{}".format(urljoin(link, "search/rrr"))
    return link


def get_resume_links(resp):
    resume_link_xp = '//a[@class="hdrlnk"]/@href'
    links = []
    for link in resp.xpath(resume_link_xp):
        link = link.extract()

        if link.startswith("/res"):
            link = urljoin(resp.url, link)
            links.append(link)

    return links


def validate_page(spider, response):

    spider.logger.debug("\n### Validate: ({}) ###\n".format(response))

    try:
        title = response.xpath("//title/text()").extract()[0]
        spider.logger.debug("### Response title: [{}] ###".format(title))
        # print(response.body)

        footer_info_xp = "//span[@class='desktop']/text()"
        footer_info = response.xpath(footer_info_xp).extract()[0]
        spider.logger.info("#### Footer info: [{}] ####\n".format(footer_info))
    except IndexError:
        spider.logger.warning("Validation error: {},\
 fetch again...".format(response.url))
        return False

    return True


def get_redirect_link(spider, response):
    """ Returns string for Request """

    location = response.headers.get("Location").decode("utf-8")
    redirect_msg = "---> Trying to redirect from: ({}) to: ({})"
    new_url = urljoin(response.url, location)
    spider.logger.debug(redirect_msg.format(response.url, new_url))

    if location.startswith("http"):
        spider.logger.warning("*** Don't redirect to: {}\n\n".format(location))
        return False

    return new_url


def get_callback(spider, request, response):
    if request.url == "http://www.craigslist.org/about/sites?lang=en&cc=us":
        return spider.parse

    elif re.search(r"search/rrr$", request.url):
        return spider.parse_resume_list

    elif re.search(r"res\/\d+.html$", request.url):
        return spider.parse_resume


def generate_ua():
    return faker.user_agent()
