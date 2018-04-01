from util import Util

uti = Util()

class CrawlResult:
    def __init__(self, page_name, title, crawl_url, keyword):
        self.page_name = page_name
        self.title = title
        self.folder = page_name.split('.')[0]
        self.crawl_url = crawl_url
        self.body = ''
        self.s3_path = ''
        self.keyword = keyword
        self.has_results = False
        return
    def crawl(self):
        self.body = uti.fetch_crawl_url(self.crawl_url)
    def print_all(self):
        print self.page_name
        print self.title
        print self.crawl_url
        return 
    def check_duplicate(self):
        if(uti.check_duplicate(self.page_name)):
            return True
        return False
    def save_results(self):
        try:
            folder_path = self.folder            
            uti.get_all_css(self.body, folder_path)
            uti.get_all_images(self.body, folder_path)
            self.s3_path = s3_path = uti.save_html(self.body, folder_path)
            details = self
            uti.save_results_db(details)
        except Exception as err:
            uti.log_error(err)                
        return 
  
