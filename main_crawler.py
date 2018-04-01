from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib2 import HTTPError
from urllib2 import URLError
from subprocess import call
import re


def check_extension(link, match_type):
    # split the link about / and get the last word
    word_list = link.split('/')
    last_word = None
    if len(word_list) >= 1:
        last_word = word_list[-1]

    if last_word is not None:
        # now split the wrod about '.' and get the extension
        if '.' in last_word:
            extension = last_word.split('.')[-1]
            if extension == match_type:
                return True
    return False


def crawl_recursively(main_link, fetched_link, match_type):
    # base case: if the link has the required match_type as extension
    if check_extension(fetched_link, match_type) is True:
        # write download command
        call(['mkdir', 'crawled_files'])
        call(['wget', fetched_link, '-P', './crawled_files/'])
        print fetched_link
        return
    # recursive case: fetch the link in the current page,
    try:
        html_data = urlopen(fetched_link)
        # convert to lxml using BeautifulSoup
        bs = BeautifulSoup(html_data, 'lxml')
        # get the links
        links = bs.findAll('a', attrs={'href': re.compile('[a-zA-Z0-9_()]')})

        # now iterate over the links and
        # discard the next call if link is the pointing to some parent
        # directory in same domain, or discard if the link is same as
        # current link (this can be identified by check if it has / or not)
        for link in links:
            # get url
            url = link.get('href')
            # check if the url is complete url or reference url
            # if url starts from http(s) then its complete
            if len(url) >= 4 and url[:4] == 'http':
                # its complete url
                # discard next call if url is substring of parent_link
                if url not in fetched_link:
                    # call and update main_link and fetched_link to url
                    crawl_recursively(url, url, match_type)
            else:
                # if url == 'Slides.pdf':
                #     print 'main_link:-', main_link
                # the url is reference url so append the main url
                # Also, check if the url is pointing to parent dir or current
                # dir, then I don't need to perform next call
                # if url has no / then it is pointing to current dir
                if '/' not in url:
                    # check if the url is the required file name or not
                    if '.' in url:
                        # print 'amit:-', url
                        if '.' in url:
                            # get last part and ignore next call if it's
                            # other than match_type type, because it can be
                            # a large file will will take much time in reading
                            last_part = url.split('.')[-1]
                            if last_part == match_type:
                                up_url = main_link + '/' + url
                                crawl_recursively(up_url, up_url, match_type)
                else:
                    # now, url can be parent or can be next page, but I will
                    # append it to the main_link, so that if there it's a parent
                    # url then after appeding it will be HTTPError, else it
                    # would fetch apt
                    update_url = main_link + url  # no need to append '/'
                    crawl_recursively(update_url, update_url, match_type)
    except HTTPError:
        # print 'PAGE NOT FOUND'
        pass
    except URLError:
        # print 'urllib2.URLError: name or service not known'
        pass


if __name__ == '__main__':
    main_link = "https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1126/lectures/"
    # main_link = "http://binomial.me"
    # main_link = "https://en.wikipedia.org/wiki/Main_Page"
    crawl_recursively(main_link, main_link, 'pdf')
