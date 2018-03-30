from bs4 import BeautifulSoup
from urllib2 import urlopen
import re


def crawl_recursively(main_link, fetched_link, match_type):
    # check if fetched_link contains complete link address or not
    # if fetched_link doesn't contains the complete address then append
    # the home address to it, else work with same fetched_link
    # I am assuming that I will be lucky enough to not get any findname
    # starting with 'http'
    if fetched_link[:4] != 'http':
        fetched_link = main_link + '/' + fetched_link

    # get the html data
    html_data = urlopen(fetched_link)
    # convert to lxml
    bs = BeautifulSoup(html_data, 'lxml')

    # get the links, the regular expression will be dynamic in nature so,
    # make sure that gets passed by the client in production
    links = bs.findAll('a', attrs={'href': re.compile('[a-zA-Z0-9_()]')})

    for link in links:
        url_ = link.get('href')
        if '/' in url_:
            last_word = url_.split('/')[-1]
            if last_word is not None:
                # since, last word is not none, so it can be a file name or
                # it can be just a directory in the url path
                # if it contains the last extension as the match_type then
                # it's the file, else its just another dir in url path
                exten = last_word.split('.')
                if exten[-1] is not None:
                    if exten[-1] == match_type:
                        # it matches the extension so download the file
                        print last_word
                        pass
                    else:
                        # doesn't match the match_type so call it recursively
                        crawl_recursively(main_link, url_, match_type)
            else:
                # the last_word is None, so get the second last word because
                # after that there is possiblity of getting the file
                word = url_.split('/')[-2]
                crawl_recursively(main_link, word, match_type)
        else:
            print 'no'
        # print link.get('href')


if __name__ == '__main__':
    main_link = "https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1126/lectures/"
    # main_link = "http://binomial.me"
    # main_link = "https://en.wikipedia.org/wiki/Main_Page"
    crawl_recursively(main_link, main_link, 'pdf')
