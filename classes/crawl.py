from util import Util
from crawl_result import CrawlResult

uti = Util()

class Crawl:
    def __init__(self, key_word, crawl_url):
        self.body = ""
        self.key_word = key_word
        self.crawl_url = crawl_url
        self.has_results = False
    def fetch(self):
        try:
            self.body = uti.fetch_crawl_url(self.crawl_url)
            self.scan_for_key_word()
        except Exception as err:
            uti.log_error(err)
    def scan_for_key_word(self):
        try:
            soup = self.body
            results = soup.findAll('a', {'class': 'result-title'})
            if(len(results) != 0):
                self.has_results = True
                for result in results:
                    title = result.string
                    href = result.get('href')
                    page_name = href.split("/").pop()
                    crawl_result = CrawlResult(page_name, title, href, self.key_word)
                    crawl_result.crawl()
                    if(not crawl_result.check_duplicate()):
                        crawl_result.save_results()
            else:
                print 'no results for:', self.key_word 
                return False
        except Exception as err:
            uti.log_error(err)
            return False
    def check_duplicate_result(self):
        # check database for duplicate page_name
        # if exists, do nothing
        # else call save function
        return
    def print_all(self):
        print self.key_word
        print self.crawl_url
    def message_user():
        # send message that result is found
        return
    def save(self):
        # save page_name, url to database
        # save body to s3
        return
