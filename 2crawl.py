from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib2 import HTTPError
import re


def crawl_recursively(main_link, fetched_link, match_type):
    # check if fetched_link contains complete link address or not
    # if fetched_link doesn't contains the complete address then append
    # the home address to it, else work with same fetched_link

    if len(fetched_link) >= 4:
        if fetched_link[:4] != 'http':
            fetched_link = main_link + '/' + fetched_link
    print 'fetched_link:', fetched_link

    try:
        html_data = urlopen(fetched_link)
        bs = BeautifulSoup(html_data, 'lxml')
        links = bs.findAll('a', attrs={'href': re.compile('[a-zA-Z0-9_()]')})
        for link in links:
            if '/' in link:
                url_ = link.get('href')
                print url_
                if url_ is not None:
                    crawl_recursively(main_link, url_, match_type)
            else:
                # print 'no slash'
                print link
    except HTTPError:
        print 'NOT FOUND'


if __name__ == '__main__':
    main_link = "https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1126/lectures/"
    # main_link = "http://binomial.me"
    # main_link = "https://en.wikipedia.org/wiki/Main_Page"
    crawl_recursively(main_link, main_link, 'pdf')
