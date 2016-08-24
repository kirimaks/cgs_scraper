from urllib.parse import urljoin
import requests


def make_resume_list_link(link):
    link = link.extract()
    link = "http:{}".format(urljoin(link, "search/rrr"))
    return link


def get_resume_links(resp):
    resume_link_xp = '//a[@class="hdrlnk"]/@href'
    links = []
    for link in resp.xpath(resume_link_xp):
        link = link.extract()

        # if link.startswith("/res"):
        link = urljoin(resp.url, link)
        links.append(link)

    return links


def validate_page(spider, response):

    spider.logger.debug("\n### Validate: ({}) ###\n".format(response))

    try:
        title = response.xpath("//title/text()").extract()[0]
        spider.logger.debug("### Response title: [{}] ###".format(title))
        print(response.body)

        footer_info_xp = "//span[@class='desktop']/text()"
        footer_info = response.xpath(footer_info_xp).extract()[0]
        spider.logger.info("#### Footer info: [{}] ####\n".format(footer_info))
    except IndexError:
        spider.logger.warning("Validation error: {},\
 fetch again...".format(response.url))
        return False

    return True


def check_proxy(proxy):
    # TODO: write re template for checking

    if "undef" not in proxy:
        return True

    return False


def generate_proxy(spider, attemp_num):
    """ Return a string in curl style """

    proxy_api1 = "https://mighty-ridge-44958.herokuapp.com/get_proxy"
    proxy_api2 = "http://gimmeproxy.com/api/getProxy?protocol=http"

    while True:     # Generate proxy and test it.
        if (attemp_num > 0) and (attemp_num % 5 == 0):
            try:
                proxy = requests.get(proxy_api2).json()['curl']
            except:
                pass
        proxy = requests.get(proxy_api1).text

        if check_proxy(proxy):
            # If test is passed, stop it and continue
            # with this proxy.
            break

    spider.logger.debug("*** NEW PROXY ***: ({})".format(proxy))
    return proxy


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

    elif request.url.endswith("craigslist.org/search/rrr"):
        return spider.parse_resume_list
