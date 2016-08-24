from scrapy import Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from faker import Factory
import tools

faker = Factory().create()


class RandomProxy:
    def process_request(self, request, spider):
        spider.logger.debug("*** New Request ***\n({})\n".format(request.url))

        proxy = tools.generate_proxy(spider,
                                     request.meta.get('retry_times', 0))
        request.meta['proxy'] = proxy

        return None  # Continue this request.

    def process_response(self, request, response, spider):
        spider.logger.debug("Response: ({})".format(response))

        # Get callback before.
        callback = tools.get_callback(spider, request, response)

        # If http code is 200, need to validate the page.
        if response.status == 200:
            if not tools.validate_page(spider, response):
                return Request(response.url,
                               dont_filter=True,
                               callback=callback)

        elif response.status in spider.handle_httpstatus_list:
            new_url = tools.get_redirect_link(spider, response)
            if not new_url:
                return Request(response.url,
                               dont_filter=True,
                               callback=callback)

            return Request(new_url)

        return response


class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', faker.user_agent())
