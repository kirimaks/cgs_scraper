from urllib.parse import urljoin


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
