import requests
from scrapy import Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from faker import Factory

faker = Factory().create()


def validate_page(spider, response):
    title = response.xpath("//title/text()").extract()[0]
    spider.logger.info("\nResponse title: [{}]".format(title.strip()))

    '''
    footer_info_xp = "//span[@class='desktop']/text()"
    footer_info = response.xpath(footer_info_xp).extract()[0]
    spider.info("\nFooter infoL [{}]\n".format(footer_info))
    '''


def generate_proxy(attemp_num):
    """ Return a string in curl style """

    # proxy_api_url1 = "https://mighty-ridge-44958.herokuapp.com/get_proxy"
    px_api_url1 = "https://mighty-ridge-44958.herokuapp.com/get_proxy/plain/https"
    px_api_url2 = "http://gimmeproxy.com/api/getProxy?protocol=https"
    px_api_url3 = "http://gimmeproxy.com/api/getProxy?anonymityLevel=1"

    if (attemp_num > 0) and (attemp_num % 5 == 0):
        try:
            return requests.get(px_api_url3).json()['curl']
            return requests.get(px_api_url2).json()['curl']
        except:
            pass

    return requests.get(px_api_url1).text


class RandomProxy:

    def process_request(self, request, spider):
        spider.logger.debug("*** New Request ***\n({})\n".format(
                            request.url))

        # Generate new proxy.
        proxy = generate_proxy(request.meta.get('retry_times', 0))
        spider.logger.debug("*** NEW PROXY ***: ({})".format(proxy))
        request.meta['proxy'] = proxy

        return None  # Continue this request.

    def process_response(self, request, response, spider):
        """ Vaidate page """

        # TODO: make separate function for validation.

        try:
            validate_page(spider, response)

        except IndexError:
            spider.logger.warning("\n<<< Not valid page, fetch again >>>\n")
            return Request(response.url, dont_filter=True,
                           meta=dict(dont_redirect=True))

        return response


class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', faker.user_agent())
